package xyz.retrixe;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.MapWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import xyz.retrixe.mappers.*;
import xyz.retrixe.reducers.ElasticSumReducer;
import xyz.retrixe.reducers.SumReducer;

public class Main {

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = new Job(conf, "HTTP Server Logs Analysis MapReduce");
        job.setJarByClass(Main.class);

        if (args.length < 3) {
            throw new RuntimeException("Valid args: <operation> " +
                    "<input: path in HDFS> <output: path in HDFS, or 'elasticsearch'>");
        }
        String elasticsearchResource;
        switch (args[1]) {
            case "urlCount":
                elasticsearchResource = "url_count";
                job.setMapperClass(URLCountMapper.class);
                break;
            case "statusCodeCount":
                elasticsearchResource = "status_code_count";
                job.setMapperClass(StatusCodeCountMapper.class);
                break;
            case "dailyCount":
                elasticsearchResource = "daily_count";
                job.setMapperClass(DailyCountMapper.class);
                break;
            case "hourlyCount":
                elasticsearchResource = "hourly_count";
                job.setMapperClass(HourlyCountMapper.class);
                break;
            case "dailyHourlyCount":
                elasticsearchResource = "daily_hourly_count";
                job.setMapperClass(DailyHourlyCountMapper.class);
                break;
            default:
                throw new RuntimeException("Invalid operation! Valid operations: " +
                        "urlCount, statusCodeCount, dailyCount, hourlyCount, dailyHourlyCount");
        }
        if (args[3].startsWith("elasticsearch")) {
            job.setReducerClass(ElasticSumReducer.class);
            job.setMapOutputValueClass(IntWritable.class);
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(MapWritable.class);
        } else {
            job.setReducerClass(SumReducer.class);
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(IntWritable.class);
        }
        FileInputFormat.addInputPath(job, new Path(args[2]));
        if (args[3].startsWith("elasticsearch")) {
            job.setOutputFormatClass(org.elasticsearch.hadoop.mr.EsOutputFormat.class);
            job.getConfiguration().set("es.resource", elasticsearchResource);
            job.getConfiguration().set("es.nodes", "host.containers.internal");
            job.getConfiguration().set("es.port", "9200");
            job.getConfiguration().set("es.nodes.discovery", "false");
            job.getConfiguration().set("es.nodes.wan.only", "true");
            job.getConfiguration().set("es.net.http.auth.user", "elastic");
            job.getConfiguration().set("es.net.http.auth.pass", "02LKhXlV");
        } else {
            FileOutputFormat.setOutputPath(job, new Path(args[3]));
        }
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
