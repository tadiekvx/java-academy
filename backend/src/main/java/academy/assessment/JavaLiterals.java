package academy.assessment;

import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

/**
 * Turns YAML test values into Java source literals of a declared parameter or return type.
 * Supports the types beginner exercises need: primitives, {@code String}, one-dimensional arrays
 * of those, and {@code List}/{@code ArrayList} of boxed types or {@code String}.
 */
public final class JavaLiterals {

    private static final Pattern LIST_TYPE = Pattern.compile("(List|ArrayList)<(\\w+)>");
    private static final Map<String, String> BOXED = Map.of(
            "Integer", "int", "Long", "long", "Double", "double", "Boolean", "boolean", "Character", "char", "String", "String");
    private static final List<String> SCALARS = List.of("int", "long", "double", "boolean", "char", "String");

    private JavaLiterals() {}

    public static boolean isSupported(String type) {
        if (SCALARS.contains(type)) {
            return true;
        }
        if (type.endsWith("[]")) {
            return SCALARS.contains(type.substring(0, type.length() - 2));
        }
        Matcher m = LIST_TYPE.matcher(type);
        return m.matches() && BOXED.containsKey(m.group(2));
    }

    /** A class literal for the erased type, e.g. {@code int[].class} or {@code java.util.List.class}. */
    static String classLiteral(String type) {
        Matcher m = LIST_TYPE.matcher(type);
        if (m.matches()) {
            return "java.util." + m.group(1) + ".class";
        }
        return type + ".class";
    }

    static String literal(Object value, String type) {
        if (value == null) {
            if (SCALARS.contains(type) && !type.equals("String")) {
                throw new IllegalArgumentException("null is not a valid " + type);
            }
            return "null";
        }
        Matcher listType = LIST_TYPE.matcher(type);
        if (listType.matches()) {
            String element = listType.group(2);
            List<?> items = asList(value, type);
            if (items.isEmpty()) {
                return "new java.util.ArrayList<" + element + ">()";
            }
            return "new java.util.ArrayList<" + element + ">(java.util.Arrays.<" + element + ">asList("
                    + items.stream().map(v -> literal(v, BOXED.get(element))).collect(Collectors.joining(", ")) + "))";
        }
        if (type.endsWith("[]")) {
            String element = type.substring(0, type.length() - 2);
            return "new " + type + " {" + asList(value, type).stream()
                    .map(v -> literal(v, element)).collect(Collectors.joining(", ")) + "}";
        }
        return switch (type) {
            case "int" -> Integer.toString(number(value, type).intValueExact());
            case "long" -> number(value, type).longValueExact() + "L";
            case "double" -> doubleLiteral(number(value, type).doubleValue());
            case "boolean" -> {
                if (!(value instanceof Boolean b)) {
                    throw new IllegalArgumentException(value + " is not a boolean");
                }
                yield b.toString();
            }
            case "char" -> {
                String s = String.valueOf(value);
                if (s.length() != 1) {
                    throw new IllegalArgumentException("\"" + s + "\" is not a single char");
                }
                yield "'" + escape(s, '\'') + "'";
            }
            case "String" -> "\"" + escape(String.valueOf(value), '"') + "\"";
            default -> throw new IllegalArgumentException("Unsupported type " + type);
        };
    }

    private static java.math.BigDecimal number(Object value, String type) {
        if (!(value instanceof Number n)) {
            throw new IllegalArgumentException(value + " is not a number (expected " + type + ")");
        }
        return new java.math.BigDecimal(n.toString());
    }

    private static String doubleLiteral(double d) {
        if (Double.isNaN(d)) {
            return "Double.NaN";
        }
        if (Double.isInfinite(d)) {
            return d > 0 ? "Double.POSITIVE_INFINITY" : "Double.NEGATIVE_INFINITY";
        }
        return Double.toString(d);
    }

    private static List<?> asList(Object value, String type) {
        if (!(value instanceof List<?> list)) {
            throw new IllegalArgumentException(value + " is not a list (expected " + type + ")");
        }
        return list;
    }

    private static String escape(String s, char quote) {
        StringBuilder b = new StringBuilder();
        for (char c : s.toCharArray()) {
            switch (c) {
                case '\\' -> b.append("\\\\");
                case '\n' -> b.append("\\n");
                case '\r' -> b.append("\\r");
                case '\t' -> b.append("\\t");
                default -> {
                    if (c == quote) {
                        b.append('\\').append(c);
                    } else if (c < 0x20) {
                        b.append(String.format("\\u%04x", (int) c));
                    } else {
                        b.append(c);
                    }
                }
            }
        }
        return b.toString();
    }
}
