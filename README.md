# Plover Application Controls
Plover plugin to monitor and control the currently active window.

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

The `{PLOVER:application}` command acts on the currently active window. It takes a subcommand as its first argument,
with further arguments separated by `:`.

For example, `{PLOVER:application:move:100:0}` will move the current window 100 pixels to the right.

| Window Command   | Description                  | Arguments           | 
|------------------|------------------------------|---------------------|
| close            |                              |                     |
| minimize         |                              |                     |
| maximize         |                              |                     |
| restore          |                              |                     |
| hide             |                              |                     |
| show             |                              |                     |
| activate         |                              |                     |
| resize           | Resize by a pixel offset     | `<x: int> <y: int>` |
| resize_to        | Resize to a set pixel size   | `<x: int> <y: int>` |
| move             | Move by a pixel offset       | `<x: int> <y: int>` |
| move_to          | Move to a set pixel location | `<x: int> <y: int>` |
| raise_window     |                              |                     |
| lower_window     |                              |                     |
| always_on_top    |                              | `[value: bool]`     |
| always_on_bottom |                              | `[value: bool]`     |
| send_behind      |                              |                     |
| accept_input     |                              | `[value: bool]`     |
