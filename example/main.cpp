#include <cstdio>

#include "../include/strc_log/strc_log.h"

// define a custom logger that will output the byte stream
void cgx::logger_handler(const std::uint8_t* bytes, std::size_t size) {
    for (std::size_t i = 0; i < size; ++i) {
        putchar(bytes[i]);
    }
}

// we can also use the logger with enums
enum class Enumerator {
    ItCanBeVeryVerbose,
};

int main() {
    CGX_INFO("The following log levels are available:");
    CGX_TRACE("CGX_TRACE(str)");
    CGX_USER("CGX_USER(str)");
    CGX_DEBUG("CGX_DEBUG(str)");
    CGX_INFO("CGX_INFO(str)");
    CGX_WARN("CGX_WARN(str)");
    CGX_ERROR("CGX_ERROR(str)");
    CGX_FATAL("CGX_FATAL(str)");
    CGX_LOG("CGX_LOG(str)");
    CGX_PRINT(
        "CGX_PRINT(str): this is a special case that only show the string "
        "without file and line information");

    CGX_PRINT("");
    CGX_INFO(
        "You can show compiler information like the date "
        "(" __DATE__
        ") and time "
        "(" __TIME__ ") of compilation");

    CGX_PRINT("");
    CGX_INFO("It is possible to pass variables to the log:");
    for (int i = 0; i < 3; ++i) {
        CGX_DEBUG("i = %d", i);
    }

    CGX_INFO("and use format modifiers:");
    for (float i = 0; i < 0.05; i += 0.015f) {
        CGX_DEBUG("i = %0.2f (%f)", i, i);
    }

    auto e = Enumerator::ItCanBeVeryVerbose;
    CGX_INFO(
        "We can print verbose enums using '%%s' and 'cgx::enum_arg(e)'\n"
        "e.g. e=%s",
        cgx::enum_arg(e));

    auto bytes =
        cgx::format("We can print verbose enums: %s"_strc, cgx::enum_arg(e));
    CGX_INFO(
        "Which translates to the array bytes: [%02x %02x %02x %02x]"
        " + [%02x %02x %02x %02x]",
        bytes[0], bytes[1], bytes[2], bytes[3], bytes[4], bytes[5], bytes[6],
        bytes[7]);
    CGX_INFO(
        "                                     [ string id ] + [  enum id  ]");

    CGX_INFO(
        "Because we are only streaming bytes, the transfer is very fast and "
        "small");
    CGX_INFO(
        "For example, the total transfer size of this program is %d bytes vs "
        "%.1fkB if we used strings",
        180, 2.7f);

    CGX_PRINT(
        "Try running 'build/example_logger | "
        "python3 ../tools/parse_log.py --database=\"strc.json\" --log-level 3' "
        "to hide file information and show only INFO (3) logs and higher.");
    CGX_PRINT("Run python3 ../tools/parse_log.py -h to see more options.");
}
