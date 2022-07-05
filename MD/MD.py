from hash import Hash

if __name__ == "__main__":
    hash = Hash()
    m = input("Please input message string: ")
    n = input("Please input desired length of output: ")
    n = int(n)
    #n = input("Please input desired length of hash: ")
    print("Generated hash: ", hash.hash_final(m, n= n))
