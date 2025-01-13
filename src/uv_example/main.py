from sample.repositories import UserRepository


def main():
    all_name = UserRepository.get_all_name()
    print(all_name)


if __name__ == "__main__":
    main()
