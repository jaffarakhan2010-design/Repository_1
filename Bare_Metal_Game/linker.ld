/* Set the entry point of the program */
ENTRY(_start)

SECTIONS
{
    /* Starts at the Raspberry Pi 5 64-bit load address */
    . = 0x80000;

    .text : {
        /* Keep _start at the very top of the binary */
        KEEP(*(.text._start))
        *(.text)
    }

    /* Align to 16 bytes for the Mailbox structures in your data */
    .data : ALIGN(16) {
        *(.data)
    }

    .bss : {
        *(.bss)
    }
}