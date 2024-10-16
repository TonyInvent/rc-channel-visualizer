# RC Channel Data Visualizer

This Python application provides a real-time graphical user interface for visualizing RC (Radio Control) channel data that has been preprocessed by an STM32 microcontroller. It reads serial output from the MCU, which parses CRSF (Crossfire) data and sends it over UART, and displays the values of 16 channels using progress bars and numerical labels.

## Features

- Real-time visualization of 16 RC channels
- Progress bars for visual representation of channel values
- Numerical display of exact channel values
- Multi-threaded design for efficient data processing and GUI updates
- Serial port communication for data input from STM32 MCU

## Requirements

- Python 3.x
- tkinter
- pyserial

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/TonyInvent/rc-channel-visualizer.git
   ```

2. Install the required packages:
   ```
   pip install pyserial
   ```

## Usage

1. Ensure your STM32 MCU is set up to parse CRSF data and output it via UART in the following format:
   ```c
   printf("channel_values data:\r\n");
   for (int i = 0; i < CRSF_NUM_CHANNELS; i++)
   {
       printf("Channel %d: %d\r\n", i, channel_values[i]);
   }
   printf("\r\n");
   ```

2. Connect the UART output of your STM32 MCU to your computer's COM port.

3. Update the COM port in the code if necessary:
   ```python:channel_viz.py
   self.uart = serial.Serial('COM5', 468000, timeout=1)
   ```

4. Run the script:
   ```
   python channel_viz.py
   ```

5. The GUI will open, displaying real-time data from your STM32 MCU.

## How It Works

1. The STM32 MCU parses CRSF data and sends it over UART.
2. The Python application initializes a serial connection to the specified COM port.
3. It starts two threads:
   - One for reading serial data from the MCU
   - Another for processing the received data
4. The main thread updates the GUI with the processed data.
5. Channel values are displayed both as progress bars and numerical values.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/rc-channel-visualizer/issues) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)
