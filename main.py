"""
Description:
Program intended to act as a testing aid for another project.
Program reads and prints Bar Codes on provided .pdf files
"""

import os, argparse
import logging as log
from pathlib import Path

# BAR CODE READER & DECODER
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
from PIL import Image
from pypdf import PdfReader

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


###############################################################################################
###############################################################################################
###############################################################################################


args = argparse.ArgumentParser()
args.add_argument(
  "-t",
  "--test",
  type=int,
  help="Declair if the application should run in test mode [0 -> production (default) | 1 -> test mode]."
)

args = args.parse_args()


###############################################################################################
###############################################################################################
###############################################################################################


# Searches a given page of a .pdf file for valid Bar Codes and returns the value contained within 
def barCodeSearch(pdf, index):

  # Found dpi = 200 to be prefectly fine for program needs
  pages = convert_from_path(
    pdf, 
    dpi=200, 
    poppler_path=str(Path().absolute()) + "\\poppler-25.07.0\\Library\\bin" # Path to local installation of Poppler needed to convert .pdf file to scanable image
    )

  # Sets page being scanned based off of the currently read page index
  image = pages[index]

  # saves image generated for debugging
  image.save("./images/" + pdf.split("/")[-1].split(".pdf")[0] + str(index) + ".png")

  results = decode(image)

  # Grabs Bar Code value from first scan on the page

  if results:
    print(results[0].data.decode("utf-8"), flush=True)
  # if results:
  #     out = results[0].data.decode("utf-8")
  # else:
  #     out = "FF-00000"

  # return out


# Parses given .pdf files into single page files
def PDFsplit(pdf):
  icon = ["|", "/", "\\"]
  # starting index of first slice
  index = 0

  # creating pdf reader object
  try:
    reader = PdfReader(pdf)
  except Exception as e:
    log.error("ERROR with: " + str(pdf) + " | " + str(e))
    print("ERROR with: " + str(pdf) + " | " + str(e))
    return

  print("Reading File: " + pdf, flush=True)
  log.info("Reading File: " + pdf)

  # loops through each page of .pdf file
  while index < len(reader.pages):
    # Decodes the Bar Codes found on a given (index) .pdf page and returns the value of the Bar Code
    bar_code_value = barCodeSearch(pdf, index)

    # logs page info
    out_pdf = pdf.split("/")[-1]
    log.info(f"File: {out_pdf} | Page: {index+1} | Code Found: {bar_code_value}")
    
    # Provides feedback to user that the program is functioning
    print("Scanned: " + str(index + 1) + " " 
        + str(icon[index % 3]) + " " 
        + str(len(reader.pages))
        + "            ", 
        flush=True, 
        end='\r'
      )

    index += 1


def main():
  # Location of .pdf(s) being read
  search_location = "./files"

  # Searches for users Poppler folder to ensure they have the dependancy installed
  poppler_folder_name = ""
  for i in next(os.walk('.'))[1]:
    if "poppler" in i:
      poppler_folder_name = i



  # program runs through all files in search_location
  i = 0
  while i < len(os.listdir(search_location)):
    if os.listdir(search_location)[i].endswith('.pdf'):
      print("File Found: " + str(os.listdir(search_location)[i]))
      log.info("File Found: " + str(os.listdir(search_location)[i]))

      PDFsplit(search_location + "/" + os.listdir(search_location)[i])

    i += 1

  print("\nExecution Complete!", flush=True)


if __name__ == "__main__":
  # calling the main function
  main()


log.critical("### ### ### ^ Program Terminated ^ ### ### ###")
