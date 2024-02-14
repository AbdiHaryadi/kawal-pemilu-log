# Kawal Pemilu Log

This simple program is used to fetch data from [KawalPemilu](https://kawalpemilu.org), opening a chance to do further analysis. This program is only useful in Pemilu day, and will no longer be used after that (except for taking the final result).

In this program, my full scope is only for Makassar City. For higher level, I just take the overview. The full scope can be changed for other cities or regencies. To do this, you can change the `kota_id` in `config.json`. You can also change the `prov_id` for take a different province for review, instead of South Sulawesi. For time interval, I choose 10 minutes for each fetch, fair enough for 171 requests to avoid spamming. You can change `interval_seconds` for other time interval.

## How to Use
1. Make sure Python has been installed.
2. Create `private` folder in root. Inside of `private` folder, create `data` folder and `log` folder.
3. Change `config.json`, depends on the requirement.
4. Run `py main.py`.
5. To stop the program, hit "Ctrl+C".
