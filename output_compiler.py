"""
Description:
  Program runs through successful file reads and compiles them into a list of settings that can then be used
    to determin working settings for bar code detection
"""

import os, argparse
import logging as log


path = os.path.dirname(os.path.abspath(__file__)) + '\\Log\\template.log'

log.basicConfig(
    filename= path,
    level=log.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# log.debug("debug message")
# log.info("info message")
# log.warning("warning message")
# log.error("error message")
# log.critical("critical message")

log.critical("### ### ### V Program Starts V ### ### ###")

def parse_file_name(file_name):
  print(file_name)


def main():
  # Location of .pdf(s) being read
  search_location = "./images"


  # program runs through all files in search_location
  i = 0
  while i < len(os.listdir(search_location)):
    if os.listdir(search_location)[i].endswith('.png'):
      # print("File Found: " + str(os.listdir(search_location)[i]))
      log.info("[output_compiler] File Found: " + str(os.listdir(search_location)[i]))

      parse_file_name(os.listdir(search_location)[i])
    i += 1


if __name__ == "__main__":
  # calling the main function
  main()

log.critical("### ### ### ^ Program Terminated ^ ### ### ###")
