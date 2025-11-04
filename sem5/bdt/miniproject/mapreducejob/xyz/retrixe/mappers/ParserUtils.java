package xyz.retrixe.mappers;

import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoField;
import java.util.Locale;
import java.util.regex.Pattern;

public class ParserUtils {

    // Regex to parse Combined Log Format
    // 1:IP, 2:User, 3:Auth, 4:Timestamp, 5:Request (6: Method, 7: Resource, 8: HTTP Version), 9:Status, 10:Bytes
    static final Pattern logPattern = Pattern.compile(
            "^(\\S+) (\\S+) (\\S+) \\[([\\w:/]+\\s[+\\-]\\d{4})] \"(\\S+) (\\S+) (\\S+)\" (\\d{3}) (\\S+)$"
    );

    static String reformatLogDate(String date) {
        String[] splitDate = date.split("/");
        int month = DateTimeFormatter
                .ofPattern("MMM")
                .withLocale(Locale.ENGLISH)
                .parse(splitDate[1])
                .get(ChronoField.MONTH_OF_YEAR);
        return splitDate[2] + "-" + String.format("%02d", month) + "-" + splitDate[0];
    }
}
