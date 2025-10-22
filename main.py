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

from pyzxing import BarCodeReader

# SCAN POST-PROCESSING
import cv2
import numpy as np
from io import BytesIO


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

args = argparse.ArgumentParser()

"""
Name: [status]_kernel_[x]-[y]_close[z]_open[za]
Example: success_kernel[1]-[3]_close[2]_open[1]
"""

output_settings = [["kernelx", "kernely", "close", "open", "alpha", "beta"]]


###############################################################################################
###############################################################################################
###############################################################################################

# Post-processes image to increase likelihood of Bar Codes being correctly identified
def postProcessBarCode(image, index, output_location, settings):
  # Converts `image` into .png file format without writing
  png_buffer = BytesIO()
  image.save(png_buffer, format="PNG")
  image = png_buffer.getvalue()
  image = Image.open(BytesIO(image))


  image = cv2.cvtColor(np.array(image), cv2.IMREAD_GRAYSCALE)
  # image = cv2.convertScaleAbs(image, alpha=settings["alpha"], beta=settings["beta"])
  # image = cv2.equalizeHist(image)
  kernel = np.ones((settings["kernelx"], settings["kernely"]), np.uint8)       # try (3,3) or (5,5)
  image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=settings["close"])

  # Cleans up isolated specs on image
  image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=settings["open"])

  # cv2.imwrite(output_location + "/test" + str(index) + ".png", image)
  # print(image, flush=True)



  reader = BarCodeReader()
  # results = reader.decode("./read.png", try_harder=False, possible_formats=None, pure_barcode=False)
  results = reader.decode_array(image)
  results = decode(Image.fromarray(image))

  # print(results, flush=True)

  output_file_name = ""
  if results:
    output_file_name = "success"
    output_file_name += "_kernel_[" + str(settings["kernelx"]) + "]-[" + str(settings["kernely"]) + "]_close[" + str(settings["close"]) + "]_open[" + str(settings["open"]) + "]_alpha[" + str(settings["alpha"]) + "]_beta[" + str(settings["beta"]) + "]"
    # Name: [status]_kernel_[x]-[y]_close[z]_open[za]
    cv2.imwrite(output_location + "/" + output_file_name + ".png", image)
            
    # np.savetxt('test_settings1.csv', (), delimiter=',', fmt='%s')
    output_settings.append([str(settings["kernelx"]), str(settings["kernely"]), str(settings["close"]), str(settings["open"]), str(settings["alpha"]), str(settings["beta"])])


# Searches a given page of a .pdf file for valid Bar Codes and returns the value contained within 
def barCodeSearch(pdf, index, output_location):

  # Found dpi = 200 to be prefectly fine for program needs
  pages = convert_from_path(
    pdf, 
    dpi=200, 
    poppler_path=str(Path().absolute()) + "\\poppler-25.07.0\\Library\\bin" # Path to local installation of Poppler needed to convert .pdf file to scanable image
    )
  

  # Sets page being scanned based off of the currently read page index
  image = pages[index]
  # w, h = image.size
  # # Specifying location to look for Bar Codes
  # crop_box = (int(w*0.1), int(h*0.80), w, h)  # (left, top, right, bottom)
  # image = image.crop(crop_box)

  # results = postProcessBarCode(image, index, output_location)

  # print(results, flush=True)

  # Grabs Bar Code value from first scan on the page
  # if results:
  #     out = results[0].data.decode("utf-8")
  # else:
  #     out = "FF-00000"


  kernelx = 0
  kernely = 0
  close = 0
  _open = 0
  alpha = 0.0
  beta = 0.0
  while kernelx < 6:
    while kernely < 6:
      while close < 6:
        while _open < 6:
          settings = {
            "status": "",
            "kernelx": kernelx,
            "kernely": kernely,
            "close": close,
            "open": _open,
            "alpha": alpha,
            "beta": beta
          }

          postProcessBarCode(image, index, output_location, settings)
          # while alpha <= 3.0:
          #   while beta <= 1.0:
          #     beta += 0.1
          #   alpha += 0.1
          _open += 1
          alpha = 0.0
          beta = 0.0
        close += 1
        _open = 0
        alpha = 0.0
        beta = 0.0
      kernely += 1
      close = 0
      _open = 0
      alpha = 0.0
      beta = 0.0

    kernelx += 1
    kernely = 0
    close = 0
    _open = 0
    alpha = 0.0
    beta = 0.0




  # print(results, flush=True)



# Parses given .pdf files into single page files
def PDFsplit(pdf, output_location):
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
    bar_code_value = barCodeSearch(pdf, index, output_location)

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
  output_location = "./images"



  # program runs through all files in search_location
  i = 0
  while i < len(os.listdir(search_location)):
    if os.listdir(search_location)[i].endswith('.pdf'):
      # print("File Found: " + str(os.listdir(search_location)[i]))
      log.info("File Found: " + str(os.listdir(search_location)[i]))

      PDFsplit(search_location + "/" + os.listdir(search_location)[i], output_location)

    i += 1

  np.savetxt('test_settings1.csv', (output_settings), delimiter=',', fmt='%s', newline='|\n')

if __name__ == "__main__":
  # calling the main function
  main()


log.critical("### ### ### ^ Program Terminated ^ ### ### ###")
