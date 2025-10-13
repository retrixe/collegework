package xyz.retrixe.collegework;

import com.maxmind.db.MaxMindDbConstructor;
import com.maxmind.db.MaxMindDbParameter;
import com.maxmind.db.Reader;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.Topology;
import org.apache.kafka.streams.kstream.KStream;

import java.io.File;
import java.io.IOException;
import java.net.InetAddress;
import java.nio.file.Path;
import java.util.List;
import java.util.Properties;
import java.util.concurrent.CountDownLatch;
import java.util.regex.Pattern;

public class Main {
    private static final Pattern JOIN_REGEX = Pattern.compile("\\[connected player] (\\w+) \\(/(\\d+\\.\\d+\\.\\d+\\.\\d+):\\d+\\) has connected.*\"timestamp\":\"(.*)\"");
    private static final Pattern LEAVE_REGEX = Pattern.compile("\\[connected player] (\\w+) \\(/(\\d+\\.\\d+\\.\\d+\\.\\d+):\\d+\\) has disconnected.*\"timestamp\":\"(.*)\"");

    public static void main(String[] args) throws Exception {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "streams-pipe");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

        final StreamsBuilder builder = new StreamsBuilder();
        KStream<String, String> source = builder.stream("server-logs");
        source.flatMapValues(value -> {
            System.out.println(value);
            var matcher = JOIN_REGEX.matcher(value);
            if (matcher.find()) {
                var ip = matcher.group(2);
                var country = getIPInfo(ip);
                return List.of("{\"player\":\"" + matcher.group(1) + "\",\"country\":\"" + country + "\"," +
                        "\"timestamp\":\"" + matcher.group(3) + "\"}");
            } else {
                return List.of();
            }
        }).to("join-events");

        source.flatMapValues(value -> {
            System.out.println(value);
            var matcher = LEAVE_REGEX.matcher(value);
            if (matcher.find()) {
                var ip = matcher.group(2);
                var country = getIPInfo(ip);
                return List.of("{\"player\":\"" + matcher.group(1) + "\",\"country\":\"" + country + "\"," +
                        "\"timestamp\":\"" + matcher.group(3) + "\"}");
            } else {
                return List.of();
            }
        }).to("leave-events");

        final Topology topology = builder.build();
        System.out.println(topology.describe());

        final KafkaStreams streams = new KafkaStreams(topology, props);
        final CountDownLatch latch = new CountDownLatch(1);

        Runtime.getRuntime().addShutdownHook(new Thread("streams-shutdown-hook") {
            @Override
            public void run() {
                streams.close();
                latch.countDown();
            }
        });

        try {
            streams.start();
            latch.await();
        } catch (Throwable e) {
            System.exit(1);
        }
        System.exit(0);
    }

    private static final File database = Path.of("").resolve("GeoLite2-City.mmdb").toFile();

    public static String getIPInfo(String ip) {
        try (Reader reader = new Reader(database)) {
            InetAddress address = InetAddress.getByName(ip);
            LookupResult result = reader.get(address, LookupResult.class);
            return result.getCountry().getIsoCode();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public static class LookupResult {
        private final Country country;

        @MaxMindDbConstructor
        public LookupResult(@MaxMindDbParameter(name="country") Country country) {
            this.country = country;
        }

        public Country getCountry() {
            return this.country;
        }
    }

    public static class Country {
        private final String isoCode;

        @MaxMindDbConstructor
        public Country (@MaxMindDbParameter(name="iso_code") String isoCode) {
            this.isoCode = isoCode;
        }

        public String getIsoCode() {
            return this.isoCode;
        }
    }
}
