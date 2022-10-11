def extract_kbits_sum(message: int, k: int, checksum: int = 0) -> int:
    KBITS_MASK = (1 << k) - 1
    sum = message & KBITS_MASK

    for _ in range(3):
        sum += (message := message >> k) & KBITS_MASK
    sum += 2 * checksum

    overflow_bits = sum.bit_length() - k
    if overflow_bits > 0:
        sum = (sum & KBITS_MASK) + (sum >> k)

    return sum ^ KBITS_MASK


def find_checksum(s_message: int, k: int) -> int:
    return extract_kbits_sum(s_message, k)


def check_reciever_checksum(r_message: int, k: int, checksum: int) -> int:
    return extract_kbits_sum(r_message, k, checksum=checksum)


# Driver Code
def main():
    sent_message = int("10010101011000111001010011101100", 2)
    received_message = int("10010101011000111001010011101100", 2)
    k = 8

    checksum = find_checksum(sent_message, k)
    receiver_checksum = check_reciever_checksum(received_message, k, checksum)

    print("SENDER SIDE CHECKSUM: ", checksum)
    print("RECEIVER SIDE CHECKSUM: ", receiver_checksum)

    final_sum = (checksum + receiver_checksum) ^ ((1 << k) - 1)

    if final_sum == 0:
        print("Receiver Checksum is equal to 0. Therefore,")
        print("STATUS: ACCEPTED")
    else:
        print("Receiver Checksum is not equal to 0. Therefore,")
        print("STATUS: ERROR DETECTED")


if __name__ == "__main__":
    main()
