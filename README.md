# Plover Application Controls
Plover plugin to monitor and control the currently active window and switch between windows quickly.

Can also be used by other plugins to track the currently active window.

## Installation:

Navigate to the installation directory for Plover and open a terminal / command prompt.

> Run: `<exe_name> -s plover_plugins install -e plover-application-controls`

Restart Plover.

Configure > Plugins > Enable `application_controls`.

## Meta Actions:

The `{:application_name}` meta outputs information about the currently active window. Argument can be `app`, `class` or 
`title`, or a combination of them with `:` as a separator. `title` *should* be consistent between platforms, whereas 
`class` and `app` will depend across platforms and specific user installations. To find an application's `app` or 
`class`, see [meta actions](#meta-actions). `class` is only available on some Linux systems. When a property is unknown 
`UNKNOWN` will be output.

The following example will output `UNKNOWN:Navigator:Mozilla Firefox` (output will vary between platforms and 
installations). 

#### Example:
```json
{
  "W*EUPB": "{:application_name:app:class:title}"
}
```

## Commands:

The `{PLOVER:application}` can be used to change or control the currently active window. It takes a subcommand as its 
first argument, with further arguments separated by `:`.

For example, `{PLOVER:application:move:100:0}` will move the current window 100 pixels to the right.

| Window Command   | Description                                                                      | Arguments                       | 
|------------------|----------------------------------------------------------------------------------|---------------------------------|
| tab              | Focuses the nth window in history                                                | `<n: int> [initial_sync: bool]` |
| cycle            | Cycles n places through most recent windows. Chained through consecutive strokes | `<n: int> [initial_sync: bool]` |
| stop_cycle       | Terminates a cycle chain. See [cycling behaviour](#window-cycling-behaviour)     |                                 |
| sync_history     | See [syncing](#syncing)                                                          |                                 |
| close            |                                                                                  |                                 |
| minimize         |                                                                                  |                                 |
| maximize         |                                                                                  |                                 |
| restore          |                                                                                  |                                 |
| hide             |                                                                                  |                                 |
| show             |                                                                                  |                                 |
| activate         |                                                                                  |                                 |
| resize           | Resize by a pixel offset                                                         | `<x: int> <y: int>`             |
| resize_to        | Resize to a set pixel size                                                       | `<x: int> <y: int>`             |
| move             | Move by a pixel offset                                                           | `<x: int> <y: int>`             |
| move_to          | Move to a set pixel location                                                     | `<x: int> <y: int>`             |
| raise_window     |                                                                                  |                                 |
| lower_window     |                                                                                  |                                 |
| always_on_top    |                                                                                  | `[value: bool]`                 |
| always_on_bottom |                                                                                  | `[value: bool]`                 |
| send_behind      |                                                                                  |                                 |
| accept_input     |                                                                                  | `[value: bool]`                 |

### Window Cycling Behaviour:

Keys given in brackets signify a modifier key being held for the key sequence within the brackets. 
`Alt + Shift + (Tab + Tab)` means holding `Alt` and `Shift` whilst hitting `Tab` twice.

| Translated Strokes                                                                             | Equivalent keyboard input                    |
|------------------------------------------------------------------------------------------------|----------------------------------------------|
| `{PLOVER:application:tab:+1}`                                                                  | `Alt + Tab`                                  |
| `{PLOVER:application:tab:+2}`                                                                  | `Alt + (Tab + Tab)`                          |
| `{PLOVER:application:tab:-2}`                                                                  | `Alt + Shift + (Tab + Tab)`                  |
| `{PLOVER:application:tab:+1}`/`{PLOVER:application:tab:+1}`                                    | `Alt + Tab`,`Alt + Tab`                      |
| `{PLOVER:application:cycle:+1}`/`{PLOVER:application:cycle:+1}`                                | `Alt + (Tab + Tab)`                          |
| `{PLOVER:application:cycle:+2}`/`{PLOVER:application:cycle:-1}`                                | `Alt + Tab`                                  |
| `{PLOVER:application:cycle:+1}`/`normal translation`/`{PLOVER:application:cycle:+1}`           | `Alt + Tab`,`normal translation`,`Alt + Tab` |
| `{PLOVER:application:cycle:+1}{PLOVER:application:stop_cycle}`/`{PLOVER:application:cycle:+1}` | `Alt + Tab`,`Alt + Tab`                      |

#### Syncing:

If a new window appears in the background at any point without being focussed, the plugin will not be aware of its 
existence until a sync has been performed. Thus, without a sync, it will be impossible to cycle to the window. 

The `{PLOVER:application:sync_history}` command can be used to trigger a manual window sync. The `initial_sync` argument
for the `tab` and `cycle` subcommands will trigger a sync if they are first in chain. For the `tab` subcommand, this
means that a sync will always be performed before running the tab operation. For the `cycle` subcommand, this means that
a sync will be performed before the first cycle stroke, but will not be performed for subsequently chained strokes.

> **Note:** Syncs can be quite slow and may sometimes fail silently, causing Plover to hang entirely in rare cases. For 
> this reason it is recommended to have a dedicated `sync_history` stroke to be used when a window cannot be found when cycling.
