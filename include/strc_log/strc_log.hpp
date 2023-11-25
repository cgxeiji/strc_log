#pragma once

#include "../../libs/strc/strc.hpp"

namespace cgx {

extern void logger_handler(const std::uint8_t* bytes, std::size_t size);

template <typename TStrc, typename... Args>
constexpr void logger(TStrc, Args... args) {
    auto arr = cgx::format(TStrc{}, args...);
    logger_handler(arr.data(), arr.size());
}

}  // namespace cgx

#define CGX_LOGGER_NUM_TO_STR(x) #x
#define CGX_LOGGER_LINE(x) CGX_LOGGER_NUM_TO_STR(x)

#define CGX_LOG(str, ...)                                                  \
    logger("in file: " __FILE__ "@" CGX_LOGGER_LINE(__LINE__) " | "_strc + \
               str##_strc,                                                 \
           ##__VA_ARGS__)

#define CGX_PRINT(str, ...) logger(str##_strc, ##__VA_ARGS__)

#define CGX_FATAL(str, ...) CGX_LOG("[FTL] " str, ##__VA_ARGS__)
#define CGX_ERROR(str, ...) CGX_LOG("[ERR] " str, ##__VA_ARGS__)
#define CGX_WARN(str, ...) CGX_LOG("[WRN] " str, ##__VA_ARGS__)
#define CGX_INFO(str, ...) CGX_LOG("[INF] " str, ##__VA_ARGS__)
#define CGX_DEBUG(str, ...) CGX_LOG("[DBG] " str, ##__VA_ARGS__)
#define CGX_USER(str, ...) CGX_LOG("[USR] " str, ##__VA_ARGS__)
#define CGX_TRACE(str, ...) CGX_LOG("[TRC] " str, ##__VA_ARGS__)
