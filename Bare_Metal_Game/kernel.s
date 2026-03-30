.section .text
.global _start

_start:
    //Works on Raspberry Pi 5 AARCH64 - 64 bit
    //This is a Baremetal Program
    //No Library
    //Copyright by [REDACTED] 2026
    //Jaffar is Only 15
    //File Format Is Called TFP5 Created by Jaffar

    //Symbol No LED

    mov x0, #0x400000
    mov sp, x0
    sub sp, sp, #4096

    ldr x0, =0x107D517C04
    mov w1, #(1 << 10)
    str w1, [x0, #0x28] ///Clearing
    
//Get frambuffer from gpu
    ldr x0, =gpumbox
    ldr x1, =0x1000013880 //Mailbox aDDRESS GPU
    dmb sy
wait_write: 
    ldr w2, [x1, #0x18] // Checking Status is 0x18
    tst w2, #0x80000000 // IS it full
    nop
    b.ne wait_write 

    orr x0, x0, #8
    str w0, [x1, #0x20] // Send ram write 0x20
    dmb sy
wait_reply:
    ldr w2, [x1, #0x18] //ACTIVELY GETTING CURRENT INFORMATION READ is 0x00
    tst w2, #0x40000000 // Is it empty?
    b.ne wait_reply

    ldr w0, [x1, #0x00] // read response

    and w2, w0, #0xF //MASKING FOR RAM ADDRESS
    cmp w2, #8 // Is the reply for ch 8
    nop
    b.ne wait_reply // If not this wait

    dmb sy
    ldr x0, =fb_ptr
    ldr x1, [x0] //Loads GPU Address

    cbz x1, halt

//Converting for RAM
    //and x1, x1, #0x3FFFFFFF
    str x1, [x0]

loop:
    ldr x0, =0x107D517C04
    mov w1, #(1 << 23)
    str w1, [x0, #0x1C]

    ldr x0, =sky_tile
    str x0, [sp, #128]
    bl func_paint_bg

    b loop

func_paint_bg:
    mov x0, #0 // Pixel Count 0 - 63
    str x0, [sp, #16] //16
    mov x0, #0 //X coords 
    str x0, [sp, #32] // Xs 16 * 2
    mov x0, #0 // Y coords
    str x0, [sp, #48] // Ys 16

    //Tile Spefifications
    mov x0, #7 // Tile section Width
    str x0, [sp, #64] //Xe
    mov x0, #7 //Tile height max
    str x0, [sp, #80] //Ye

    //Line Vectors
    mov x0, #0 // The First X Vector
    str x0, [sp, #96]

    mov x0, #0 // First Starting Y Vector
    str x0, [sp, #112]

    func_paint_bg_ls:
        //Symbol green LED
        ldr x0, [sp, #128] // Loading tile
        ldr x1, [sp, #16] // Getting pixel counts

        ldrb w2, [x0, x1] //Storing the Value of pixel coord from tile
        ldr x0, =pallette
        lsl x2, x2, #2 //Multiplying by 4
        ldr w1, [x0, x2] //Getting the color of the pixel

        ldr x2, [sp, #48] //Calculating the coordinates
        lsl x2, x2, #8 //Multiplying by 256b
        ldr x0, [sp, #32] //Loading X offset
        add x2, x2, x0
        lsl x2, x2, #2 // Multiplying by 4 for ABRG

        ldr x0, =fb_ptr //Changing the color of 1 px
        ldr x0, [x0]
        str w1, [x0, x2]

        //Closing
        ldr x0, [sp, #16]
        add x0, x0, #1
        str x0, [sp, #16] //Pixel Count inc 1

        cmp x0, #63 //If pixel count gt 63 were done.
        b.gt func_paint_bg_paint_gl

        ldr x0, [sp, #32] // X coords inc 1
        add x0, x0, #1

        ldr x2, [sp, #96] // Getting Starting Pixel Coordinate X

        sub x2, x0, x2 //Difference between the two We  do equal because we want to paint that pixel
        ldr x1, [sp, #64]

        cmp x2, x1
        b.le x_continue // If x2 is less than x1 then continue otherwise conflict

        ldr x0, [sp, #96] //grabbing first x
        str x0, [sp, #32] //storing the new x which is reset to og 0

        ldr x0, [sp, #48] // Inc Y
        add x0, x0, #1

        ldr x2, [sp, #112] //Getting first Y

        ldr x1, [sp, #80] // Y end

        sub x2, x0, x2 //Difference between start & end

        cmp x2, x1 
        b.gt func_paint_bg_paint_gl // If y is bigger than the maximum Y value then were done.
        str x0, [sp, #48] // If were not done then continue
        b func_paint_bg_ls //Loop over again

    x_continue:
        str x0, [sp, #32]
        b func_paint_bg_ls
    func_paint_bg_paint_gl:
        ret
halt:
    //Red LED
    ldr x0, =0x107D517C04
    mov w1, #(1 << 10)
    str w1, [x0, #0x28]
    mov w1, #(1 << 11)
    str w1, [x0, #0x1C]
    b halt
.section .data

.balign 16
gpumbox:
    .word mbox_end - gpumbox //CALCULATING SPACE TOTAL SIZE
    .word 0 //Request code 0

    //Set screen 
    .word 0x00048003, 8, 8, 1440, 1080 //address gpu set screen

    //Virtual size
    .word 0x00048004, 8, 8, 256, 240

    //Depth
    .word 0x00048005, 4, 4, 32
    
    // Frame Buffer SPACE
    .word 0x00040001, 8, 4
fb_ptr:  
    .quad 0 //GPU's answer per pixel of 0,0 256 per row, and x bas on pixel basically 2d array Formula coord = ||row * 256| + colomn| * 4 |4 for AABBGGRR|
fb_size: 
    .word 0 // THis is the size of the answer

    .word 0 //end 3
mbox_end:

.balign 16

pallette:
    .word 0x00000000 //Transparent 0 
    .word 0xFFFFFFFF //White 1 
    .word 0xFFF0E0D0 // Sky 2
    .word 0xFFD0A070 // Water 3 
    .word 0xFF808080 // Rocks 4 
    .word 0xFF00FFFF // Gold Coin 5
    .word 0xFF000000 // Black 6
    .word 0xFFCC4E00 // Blue p penguin 7
    .word 0xFF00d8FF // Yellow b 8
    .word 0xFF00C7EF // Dark Yellow 9
    .word 0xFFB0B0B0 // Shadow Snow
sky_tile:
    .byte 2, 2, 2, 2, 2, 2, 2, 2
    .byte 2, 2, 2, 2, 2, 2, 2, 2
    .byte 2, 2, 2, 2, 2, 2, 2, 2
    .byte 2, 2, 2, 2, 2, 2, 2, 2
    .byte 2, 2, 2, 2, 2, 2, 2, 2
    .byte 2, 2, 2, 2, 2, 2, 2, 2
    .byte 2, 2, 2, 2, 2, 2, 2, 2
    .byte 2, 2, 2, 2, 2, 2, 2, 2
ground_tile:
    .byte 1, 1, 1, 1, 1, 1, 1, 1
    .byte 1, 1, 1, 1, 1, 1, 1, 1
    .byte 1, 1, 1, 1, 1, 1, 1, 1
    .byte 1, 1, 1, 1, 1, 1, 1, 1
    .byte 1, 1, 1, 1, 1, 1, 1, 1
    .byte 1, 1, 1, 1, 1, 1, 1, 1
    .byte 1, 1, 1, 1, 1, 1, 1, 1
    .byte 1, 1, 1, 1, 1, 1, 1, 1

//Sprites
penguinb:
    .byte 0, 0, 0, 0, 0, 0, 0, 0, 0
    .byte 0, 0, 0, 0, 0, 0, 0, 0, 0
    .byte 0, 0, 0, 0, 0, 0, 0, 0, 0
    .byte 0, 0, 0, 7, 7, 7, 7, 0, 0
    .byte 0, 0, 7, 7, 7, 7, 7, 7, 0
    .byte 0, 0, 7, 7, 6, 7, 7, 7, 0
    .byte 0, 0, 7, 7, 7, 7, 8, 8, 8
    .byte 0, 0, 7, 7, 7, 7, 7, 7, 0
    .byte 0, 7, 7, 7, 1, 1, 7, 7, 0
    .byte 7, 7, 7, 1, 1, 1, 1, 7, 7
    .byte 7, 7, 7, 1, 1, 1, 1, 7, 7
    .byte 7, 7, 1, 1, 1, 1, 1, 7, 7
    .byte 7, 7, 1, 1, 1, 1, 1, 7, 0
    .byte 0, 7, 7, 1, 1, 1, 1, 7, 0
    .byte 0, 0, 7, 1, 1, 1, 7, 0, 0
    .byte 0, 0, 8, 8, 0, 9, 9, 0, 0
