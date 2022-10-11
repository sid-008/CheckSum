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
def test_impl(sent: str, received: str) -> None:
    sent_message = int(sent, 2)
    received_message = int(received, 2)
    k = 8

    checksum = find_checksum(sent_message, k)
    receiver_checksum = check_reciever_checksum(received_message, k, checksum)

    print("SENDER SIDE CHECKSUM: ", bin(checksum)[2:])
    print("RECEIVER SIDE CHECKSUM: ", bin(receiver_checksum)[2:])

    final_sum = (checksum + receiver_checksum) ^ ((1 << k) - 1)

    if final_sum == 0:
        print("Receiver Checksum is equal to 0. Therefore,")
        print("STATUS: ACCEPTED")
    else:
        print("Receiver Checksum is not equal to 0. Therefore,")
        print("STATUS: ERROR DETECTED")
    print()


if __name__ == "__main__":
    test_impl(
        sent="10010101011000111001010011101100",
        received="10010101011000111001010011101100",
    )  # Passes
    test_impl(
        sent="10010101011000111011010011111100",
        received="10010101011000111001010011101100",
    )  # Fails
    test_impl(
        sent="10111001010100101010100010010010",
        received="10111001010100101010100010010010",
    )  # Passes
    test_impl(
        sent="10111111010110111110100010010010",
        received="10111001010100101010100010010010",
    )  # Fails
