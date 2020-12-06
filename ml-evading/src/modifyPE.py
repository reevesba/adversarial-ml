import lief
import pefile

def main():
    file = "dat/JRuler.exe"

    parsed_binary = lief.parse(file)
    pe = pefile.PE(file)

    # print number of sections with each package
    print(parsed_binary.header.numberof_sections)
    print(pe.FILE_HEADER.NumberOfSections)

    # print timestamps with each package
    print(parsed_binary.header.time_date_stamps)
    print(pe.FILE_HEADER.TimeDateStamp)

    # change the entry point
    parsed_binary.optional_header.addressof_entrypoint = 0xDEADBEEF
    pe.OPTIONAL_HEADER.AddressOfEntryPoint = 0xDEADBEEF

    # write the new file
    parsed_binary.write("dat/JRuler_altered_lief.exe")
    pe.write(filename="dat/JRuler_altered_pefile.exe")

    # verify new files for each package
    parsed_binary = lief.parse("dat/JRuler_altered_lief.exe")
    print(parsed_binary.optional_header.addressof_entrypoint)

    parsed_binary = lief.parse("dat/JRuler_altered_pefile.exe")
    print(parsed_binary.optional_header.addressof_entrypoint)

if __name__ == "__main__":
    main()
