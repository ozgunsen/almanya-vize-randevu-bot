# Almanya Schengen Vize Randevu Botu

This Python script is designed to automate the process of searching appointments for the German Schengen visa application from Turkey. It uses the Selenium WebDriver library to navigate the website, fill out appointment details, and find available appointment slots.
Important: The script is written for educational purposes.

## Prerequisites

Before using the script, make sure you have the following prerequisites installed:

- [Python 3](https://www.python.org/downloads/)
- [Selenium for Python](https://selenium-python.readthedocs.io/installation.html)
- [Playsound library (for audio alerts)](https://pypi.org/project/playsound/)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ozgunsen/almanya-vize-randevu-bot.git
   ```

2. rename _settings.py file to settings.py

3. Edit the `settings.py` file to configure the script according to your needs:

- `IDATA_URL`: The URL of the website where you want to schedule an appointment.
- `CITY`, `OFFICE`, `OFFICE_TYPE`: Values to select in the appointment form.
- `PERSONS`: A list of dictionaries containing personal information.
- `WORKING_HOURS_START` and `WORKING_HOURS_END`: Define the working hours during which the script will run.
- `WAITING_TIME`: The time to wait before retrying if no appointment is found.

4. Navigate to the project directory:

   ```bash
   cd almanya-vize-randevu
   ```

5. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script by executing the following command:

```bash
python appointment.py
```

The script will continuously monitor the website for available appointments within the specified working hours. When an appointment is found, it will play the alarm sound and stop.

## Disclaimer

This script is provided as-is, and the use of automation scripts to schedule appointments on websites may be subject to legal and ethical considerations. Use this script responsibly and in compliance with the terms of service of the website you are targeting.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

If you'd like to contribute to this project, please fork the repository and create a pull request. We welcome your contributions!