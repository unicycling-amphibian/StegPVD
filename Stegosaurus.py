#                         .       .
#                        / `.   .' \
#                .---.  <    > <    >  .---.
#                |    \  \ - ~ ~ - /  /    |
#                 ~-..-~             ~-..-~
#             \~~~\.'                    `./~~~/
#   .-~~^-.    \__/                        \__/
# .'  O    \     /               /       \  \
# (_____,    `._.'               |         }  \/~~~/
# `----.          /       }     |        /    \__/
#       `-.      |       /      |       /      `. ,~~|
#           ~-.__|      /_ - ~ ^|      /- _      `..-'   f: f:
#                |     /        |     /     ~-.     `-. _||_||_
#                |_____|        |_____|         ~ - . _ _ _ _ _>
#

##simple PVD for [1,2] matrix LSB substitution


import sys
import os
from datetime import datetime
from PIL import Image

# check hide/extract tag
global_encode_decode_flag = sys.argv[1]

# hiding global inits #filehandles #logging
if global_encode_decode_flag == '-e':

    # check for data in msg file
    if os.stat(sys.argv[3]).st_size == 0:
        sys.exit("ALERT: message file empty")

    # sysargs filehandles
    message_file = open(sys.argv[2], "r")
    print("EMBEDDING: OPENING MESSAGE FILE: ", sys.argv[2])

    cover_image = Image.open(sys.argv[3])
    print("EMBEDDING: OPENING COVER IMAGE FILE: ", sys.argv[3])

    print("EMBEDDING: CREATING STEGO IMAGE FILE: ", sys.argv[4])

    # log_file
    # script_directory = os.path.dirname(__file__)  # <-- absolute dir the script is in
    # relative_path = "log\encode_" + sys.argv[2] + "_" + sys.argv[3] + "_" + datetime.now().strftime("%Y_%m_%d%H_%M_%S") + ".log"
    # file_path = os.path.join(script_directory, relative_path)
    # log_file = open(file_path, 'w')

    # global inits

    global_embed_counter = 0

    # extract rgb image and image dimensions
    global_rgb_data = cover_image.load()
    print("EMBEDDING: RGB data extracted")

    global_image_height, global_image_width = cover_image.size
    print("EMBEDDING: image dimensions: [", global_image_height, ", ", global_image_width, "]")
    # message from utf-8 --> binary
    temp_utf_string = message_file.read()
    print("EMBEDDING: message payload size is: ", len(temp_utf_string), " utf-8 characters")
    # print("temp utf: ", temp_utf_string)
    # print("length", len(temp_utf_string))
    global_binary_payload = ''.join('{0:08b}'.format(ord(x), 'b') for x in temp_utf_string)
    # log_file.write(global_binary_payload)

    # embed payload size into message
    # payload size limit is 2^32
    global_payload_size = len(global_binary_payload)
    print("EMBEDDING: <binary> message size is: ", global_payload_size + 32, " bits  (", global_payload_size, "bits + 32-bit header )")
    # print("payload size", global_payload_size)
    binary_payload_size_32 = bin(global_payload_size)[2:].zfill(32)
    if global_payload_size >= 4294967296:
        sys.exit("EMBEDDING: ERROR: message size > header embedding capacity")
    # print("bin size bits 32: ", binary_payload_size_32)
    # log_file.write(binary_payload_size_32)
    # print("bin payload: ", global_binary_payload)
    global_binary_payload = binary_payload_size_32 + global_binary_payload
    # log_file.write(global_binary_payload)
    n = int(global_binary_payload, 2)
    # log_file.write(n.to_bytes((n.bit_length() + 7) // 8, 'big').decode())
    global_payload_size = len(global_binary_payload)

    # print("bin payload: ", global_binary_payload)
    print("EMBEDDING: message converted to binary")
    # close message after converting to bin string
    message_file.close()
    print("EMBEDDING: CLOSING MESSAGE FILE: ", sys.argv[2])


# extraction global inits filehandles and logging
elif global_encode_decode_flag == '-d':

    stego_image = Image.open(sys.argv[2])
    print("EXTRACTING: OPENING STEGO IMAGE FILE: ", sys.argv[2])
    secret_file = open(sys.argv[3], "w")
    print("EXTRACTING: OPENING SECRET FILE: ", sys.argv[2])
    # script_directory = os.path.dirname(__file__)  # <-- absolute dir the script is in
    # relative_path = "log\decode_" + sys.argv[2] + "_" + sys.argv[3] + "_" + datetime.now().strftime("%Y_%m_%d%H_%M_%S") + ".log"
    # file_path = os.path.join(script_directory, relative_path)

    # log_file = open(file_path, 'w')

    # extract rgb data and image dimensions
    global_rgb_data = stego_image.load()
    print("EXTRACTING: RGB data extracted")


    global_image_height, global_image_width = stego_image.size
    print("EXTRACTING: image dimensions: [", global_image_height, ", ", global_image_width, "]")
    global_binary_secret = ''

    stego_image.close()
    print("EXTRACTING: CLOSING STEGO IMAGE FILE: ", sys.argv[2])
else:
    print("ERROR: unexpected input ARG1: ", sys.argv[1])
    sys.exit("ERROR: ACCEPTED VALUES:  '-e', '-h' ")


# wu tsai ranges
# quantization table returns number of LSB to substitute based on PVD
def quantizationTable(channel_difference):
    if channel_difference <= 16:
        # if ___x ___[_]
        number_of_bits = 1

    elif 16 < channel_difference <= 32:
        # if __x_ __[__]
        number_of_bits = 1

    else:
        # if xx__ _[___]
        number_of_bits = 1

    # #LSB to be substituted
    return number_of_bits


# capacity function calculates embedding capacity of data in globabl_rgb_data
# returns int embedding capacity
def capacity():
    # init
    embedding_capacity = 0

    # for each reference pixel calculate its pixel pair capacity
    for image_y in range(0, global_image_height):

        # step in image_x range is the matrix size [1,2]
        for image_x in range(0, global_image_width, 2):

            # check width array out of bounds condition
            if image_x + 1 == global_image_width:
                break

            # print(image_x, image_y)

            # tuples conciliate RGBA - when RGB data has alpha channel
            tuple = global_rgb_data[image_y, image_x]
            red_reference_pixel, green_reference_pixel, blue_reference_pixel = tuple[0], tuple[1], tuple[2]

            tuple = global_rgb_data[image_y, image_x + 1]
            red_pixel, green_pixel, blue_pixel = tuple[0], tuple[1], tuple[2]

            # calculate PVD = abs(ref - target)
            red_pixel_difference = abs(red_pixel - red_reference_pixel)
            green_pixel_difference = abs(green_pixel - green_reference_pixel)
            blue_pixel_difference = abs(blue_pixel - blue_reference_pixel)

            embedding_capacity = (embedding_capacity + quantizationTable(red_pixel_difference) + quantizationTable(
                green_pixel_difference) + quantizationTable(blue_pixel_difference))
    # print(embedding_capacity)
    return embedding_capacity


# creates new pixel values by slicing reference pixel binary and message data then combining
# return new pixel values as integer
# only one pixel values is necessary, either ref or target pixel, extra pixel used in old functionality
def embedBits(channel_difference, int_reference_pixel_value, int_pixel_value):
    # global refs
    global global_binary_payload, global_embed_counter

    #increment embedded bits counter
    global_embed_counter += channel_difference
    # print("binpayload: " + global_binary_payload)
    # log_file.write(str(global_binary_payload))

    # convert to binary and pad to byte size
    binary_pixel_value = bin(int_reference_pixel_value)[2:].zfill(8)
    # remove bit positions based on quantization value
    bits_to_embed = global_binary_payload[:channel_difference]

    # print("binpixval " + binary_pixel_value + "bitstoembed " + bits_to_embed)
    # log_file.write("binpixval " + binary_pixel_value + "bitstoembed " + bits_to_embed)

    # create new pixel binary
    new_binary_pixel_value = binary_pixel_value[:len(binary_pixel_value) - len(bits_to_embed)] + bits_to_embed

    # print("newpixval " + new_binary_pixel_value)
    # print("intnewpix (ref) %s intpix %s "%(int(new_binary_pixel_value, 2), int_pixel_value))

    # log_file.write("newpixval " + new_binary_pixel_value)
    # log_file.write("intnewpix (ref) " + str(int(new_binary_pixel_value, 2)) + "intpix" + str(int_pixel_value))
    # log_file.write("chanel" + str(channel_difference) + " newdiff " + str(quantizationTable(abs(int(new_binary_pixel_value, 2) - int_pixel_value))))
    # if quantizationTable(abs(int(new_binary_pixel_value, 2) - int_pixel_value)) != channel_difference:
    #    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #    return int_reference_pixel_value

    # remove embeded pixels from message payload
    global_binary_payload = global_binary_payload[channel_difference:]
    # log_file.write("newpixval " + new_binary_pixel_value)

    # return int of binary pixel value
    return int(new_binary_pixel_value, 2)


# extracts bits from binary pixel value based on PVD
# returns extracted bits
def extractBits(channel_difference, int_pixel_value):
    # convert int pixel value to binary and pad to byte length
    binary_pixel_value = bin(int_pixel_value)[2:].zfill(8)

    # slice binary pixel value based on PVD
    extracted_bits = binary_pixel_value[len(binary_pixel_value) - channel_difference:]

    # print("binpixval ", binary_pixel_value, " channel ", channel_difference, " extracted ", extracted_bits)

    return extracted_bits


# main function
def main():
    # global includes
    global global_binary_secret, global_embed_counter, global_payload_size

    # init
    length_flag = 0
    secret_size = 0

    # encoding control loop
    if global_encode_decode_flag == '-e':
        print("EMBEDDING: COVER IMAGE FILE: embedding capacity : ", capacity(), " bits")

        # check that image capacity will support payload embedding
        if capacity() < global_payload_size:
            sys.exit("ERROR: EMBEDDING: message size > COVER IMAGE FILE capacity")

        # check that image embedding capacity will support binary size header embeding
        if capacity() < 32:
            sys.exit("ERROR: EMBEDDING: not sufficient embedding capacity for size header (32-bits)")

        # foreach matrix [1, 2] that can be formed in rgb data[]
        for image_y in range(0, global_image_height):

            # step in image_x range is the matrix size [1,2]
            for image_x in range(0, global_image_width, 2):

                # check width array out of bounds condition
                if image_x + 1 == global_image_width:
                    break

                # print(image_x, image_y)

                # tuples conciliate RGBA - when RGB data has alpha channel
                tuple = global_rgb_data[image_y, image_x]
                red_reference_pixel, green_reference_pixel, blue_reference_pixel = tuple[0], tuple[1], tuple[2]

                tuple = global_rgb_data[image_y, image_x + 1]
                red_pixel, green_pixel, blue_pixel = tuple[0], tuple[1], tuple[2]

                # calculate PVD = abs(ref - target)
                red_pixel_difference = abs(red_pixel - red_reference_pixel)
                green_pixel_difference = abs(green_pixel - green_reference_pixel)
                blue_pixel_difference = abs(blue_pixel - blue_reference_pixel)

                # print("ref pix r ", red_reference_pixel, " g ", green_reference_pixel, " b ", blue_reference_pixel)
                # print("pixel r ", red_pixel, " g ", green_pixel, " b ", blue_pixel)
                # print("pixeldifference r ", red_pixel_difference, " g ", green_pixel_difference, " b ",blue_pixel_difference)

                # calculate new pixel values with embedBits()

                # if 15 <= red_pixel_difference <= 17:
                #    new_red_pixel = embedBits(0, red_reference_pixel, red_pixel)
                # elif 33 <= red_pixel_difference <= 35:
                #    new_red_pixel = embedBits(0, red_reference_pixel, red_pixel)
                # else:
                new_red_pixel = embedBits(quantizationTable(red_pixel_difference), red_reference_pixel, red_pixel)

                # if 15 <= green_pixel_difference <= 17:
                #    new_green_pixel = embedBits(0, green_reference_pixel, green_pixel)
                # elif 28 <= green_pixel_difference <= 35:
                #    new_green_pixel = embedBits(0, green_reference_pixel, green_pixel)
                # else:
                new_green_pixel = embedBits(quantizationTable(green_pixel_difference), green_reference_pixel,
                                            green_pixel)

                # if 15 <= blue_pixel_difference <= 17:
                #    new_blue_pixel = embedBits(0, blue_reference_pixel, blue_pixel)
                # elif 28 <= blue_pixel_difference <= 35:
                #    new_blue_pixel = embedBits(0, blue_reference_pixel, blue_pixel)
                # else:
                new_blue_pixel = embedBits(quantizationTable(blue_pixel_difference), blue_reference_pixel, blue_pixel)

                # new_red_pixel = embedBits(quantizationTable(red_pixel_difference), red_reference_pixel, red_pixel)
                # new_green_pixel = embedBits(quantizationTable(green_pixel_difference), green_reference_pixel, green_pixel)
                # new_blue_pixel = embedBits(quantizationTable(blue_pixel_difference), blue_reference_pixel, blue_pixel)

                # replace rgb data with new pixel values
                global_rgb_data[image_y, image_x] = (new_red_pixel, new_green_pixel, new_blue_pixel)

                # check if binary message payload still has data

                if len(global_binary_payload) == 0:
                    print("EMBEDDING: end of <binary> message data - embedded : ", global_embed_counter, "bits")
                    print("EMBEDDING: % COVER IMAGE FILE embedding capacity used: ", global_payload_size/capacity()*100, "%")
                    # if not then save the new image with the old image header
                    cover_image.save(sys.argv[4])
                    print("EMBEDDING: WRITING STEGO IMAGE FILE: ", sys.argv[4])
                    cover_image.close()
                    print("EMBEDDING: CLOSING COVER IMAGE: ", sys.argv[3])
                    # log_file.close()
                    sys.exit("EMBEDDING: COMPLETED")

    elif global_encode_decode_flag == '-d':
        print("EXTRACTING: STEGO IMAGE FILE: embedding capacity : ", capacity(), " bits")
        for image_y in range(0, global_image_height):
            for image_x in range(0, global_image_width, 2):
                if image_x + 1 == global_image_width:
                    break

                # print(image_x, image_y)
                # log_file.write(str(image_x) + str(image_y))
                tuple = global_rgb_data[image_y, image_x]

                red_reference_pixel, green_reference_pixel, blue_reference_pixel = tuple[0], tuple[1], tuple[2]

                tuple = global_rgb_data[image_y, image_x + 1]
                red_pixel, green_pixel, blue_pixel = tuple[0], tuple[1], tuple[2]

                red_pixel_difference = abs(red_pixel - red_reference_pixel)
                green_pixel_difference = abs(green_pixel - green_reference_pixel)
                blue_pixel_difference = abs(blue_pixel - blue_reference_pixel)
                # log_file.write("r ", quantizationTable(red_pixel_difference), " g ", quantizationTable(green_pixel_difference)," b ", quantizationTable(blue_pixel_difference))
                # print("ref pix r ", red_reference_pixel, " g ", green_reference_pixel, " b ", blue_reference_pixel)
                # print("pixel r ", red_pixel, " g ", green_pixel, " b ", blue_pixel)
                # print("pixeldifference r ", red_pixel_difference, " g ", green_pixel_difference, " b ",blue_pixel_difference)

                # if not 15 <= red_pixel_difference <= 17 and not 33 <= red_pixel_difference <= 35:
                red_channel_bits = extractBits(quantizationTable(red_pixel_difference), red_reference_pixel)

                # if not 15 <= green_pixel_difference <= 17 and not 33 <= green_pixel_difference <= 35:
                green_channel_bits = extractBits(quantizationTable(green_pixel_difference), green_reference_pixel)

                # if not 15 <= blue_pixel_difference <= 17 and not 33 <= blue_pixel_difference <= 35:
                blue_channel_bits = extractBits(quantizationTable(blue_pixel_difference), blue_reference_pixel)

                # print("r ", red_channel_bits, " g ", green_channel_bits, " b ", blue_channel_bits)
                pixel_secret_bits = red_channel_bits + green_channel_bits + blue_channel_bits
                # print("secretbits ", pixel_secret_bits)
                # print("secret size", secret_size, "lengthflag", length_flag)
                # print("globalbinsec", global_binary_secret, "length", len(global_binary_secret))

                if length_flag == 0:

                    if len(global_binary_secret) >= 32:
                        bin_secret_size = global_binary_secret[:32]
                        secret_size = int(bin_secret_size, 2)
                        print("EXTRACTING: extracted <binary> message size: ", secret_size, " bits")
                        global_binary_secret = global_binary_secret[32:]
                        print("EXTRACTING: removing size header from <binary> message")
                        length_flag = 1

                global_binary_secret = global_binary_secret + pixel_secret_bits
                if length_flag == 1:
                    if len(global_binary_secret) >= secret_size:
                        global_binary_secret = global_binary_secret[:secret_size]
                        print("EXTRACTING: <binary> message extracted")
                        print("EXTRACTING: % STEGO IMAGE FILE embedding capacity used: ", secret_size / capacity() * 100, "%")
                        s = int(global_binary_secret, 2)
                        temp_bin_to_string = s.to_bytes((s.bit_length() + 7) // 8, 'big').decode()
                        print("EXTRACTING: <binary> message converted to <utf-8>")
                        secret_file.write(temp_bin_to_string)
                        print("EXTRACTING: WRITING SECRET FILE: ", sys.argv[3])

                        # log_file.close()
                        secret_file.close()
                        print("EXTRACTING: CLOSING SECRET FILE: ", sys.argv[3])
                        sys.exit("EXTRACTING: COMPLETED")


if __name__ == "__main__":
    main()
