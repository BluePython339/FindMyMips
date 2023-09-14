## FindMyMips.py - Binary Base Address Finder

This Python script, named FindMyMips.py, is designed to help you calculate the base address (load address) of a binary file by analyzing its disassembled code and searching for specific patterns in the assembly instructions. It can be particularly useful when reverse engineering binaries and determining where they are meant to be loaded in memory.

### Prerequisites

Before you get started, make sure you have the following prerequisites installed:

- Python (3.6 or higher)
- `mips-linux-gnu-objdump` (for disassembling binary files)

### Usage

1. Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/findmymips.git
```

2. Navigate to the project directory:

```bash
cd findmymips
```

3. Run the script, providing the path to your binary file as a command-line argument:

```bash
python FindMyMips.py your_binary_file.bin
```

4. The script will output the best guesses for the base address along with their corresponding scores. The top candidates are displayed, making it easier for you to identify the likely base address.

### How It Works

- The script first extracts strings from the binary file that contain the "%d" placeholder, which are often used as references for calculating base addresses.

- It then disassembles the binary file to obtain references from the assembly instructions. These references are recorded and used for base address calculations. (based on lui and addi pairs)

- A scoring mechanism is applied to different base addresses relative to the selected pivot point (a randomly chosen string containing "%d"). The score reflects the number of valid references found at each calculated base address.

- Finally, the script presents the top candidates for the base address based on their scores.

### Contributing

If you find any issues or have suggestions for improvements, please feel free to open an issue or pull request in this repository.
