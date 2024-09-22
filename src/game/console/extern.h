#pragma once

#include "game/console/common.h"

#include <stdint.h>

extern int32_t Console_GetMaxLineLength(void);
extern void Console_LogImpl(const char *text);
extern CONSOLE_COMMAND **Console_GetCommands(void);