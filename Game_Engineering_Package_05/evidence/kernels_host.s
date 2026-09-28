	.file	"kernels.cpp"
	.text
	.p2align 4
	.globl	sum_serial
	.type	sum_serial, @function
sum_serial:
.LFB15:
	.cfi_startproc
	testq	%rsi, %rsi
	je	.L7
	cmpq	$1, %rsi
	je	.L8
	movq	%rsi, %rdx
	movq	%rdi, %rax
	pxor	%xmm0, %xmm0
	shrq	%rdx
	salq	$4, %rdx
	addq	%rdi, %rdx
	.p2align 5
	.p2align 4
	.p2align 3
.L4:
	movdqu	(%rax), %xmm2
	addq	$16, %rax
	paddq	%xmm2, %xmm0
	cmpq	%rax, %rdx
	jne	.L4
	movdqa	%xmm0, %xmm1
	psrldq	$8, %xmm1
	paddq	%xmm1, %xmm0
	movq	%xmm0, %rax
	testb	$1, %sil
	je	.L1
	andq	$-2, %rsi
.L3:
	addq	(%rdi,%rsi,8), %rax
	ret
	.p2align 4,,10
	.p2align 3
.L7:
	xorl	%eax, %eax
.L1:
	ret
.L8:
	xorl	%esi, %esi
	xorl	%eax, %eax
	jmp	.L3
	.cfi_endproc
.LFE15:
	.size	sum_serial, .-sum_serial
	.p2align 4
	.globl	sum_four
	.type	sum_four, @function
sum_four:
.LFB16:
	.cfi_startproc
	cmpq	$3, %rsi
	jbe	.L32
	leaq	-4(%rsi), %r8
	pxor	%xmm0, %xmm0
	movq	%rdi, %rax
	xorl	%edx, %edx
	movq	%r8, %rcx
	movdqa	%xmm0, %xmm1
	shrq	$2, %rcx
	addq	$1, %rcx
	.p2align 5
	.p2align 4
	.p2align 3
.L18:
	movdqu	(%rax), %xmm4
	movdqu	16(%rax), %xmm5
	addq	$1, %rdx
	addq	$32, %rax
	paddq	%xmm4, %xmm1
	paddq	%xmm5, %xmm0
	cmpq	%rcx, %rdx
	jb	.L18
	movdqa	%xmm1, %xmm2
	psrldq	$8, %xmm1
	andq	$-4, %r8
	paddq	%xmm0, %xmm1
	psrldq	$8, %xmm0
	leaq	4(%r8), %rcx
	paddq	%xmm0, %xmm1
.L19:
	cmpq	%rsi, %rcx
	jnb	.L17
	subq	%rcx, %rsi
	cmpq	$1, %rsi
	je	.L20
	movq	%rsi, %rdx
	leaq	(%rdi,%rcx,8), %rax
	pxor	%xmm0, %xmm0
	shrq	%rdx
	salq	$4, %rdx
	addq	%rax, %rdx
	.p2align 5
	.p2align 4
	.p2align 3
.L21:
	movdqu	(%rax), %xmm6
	addq	$16, %rax
	paddq	%xmm6, %xmm0
	cmpq	%rax, %rdx
	jne	.L21
	movdqa	%xmm0, %xmm3
	psrldq	$8, %xmm3
	paddq	%xmm3, %xmm0
	paddq	%xmm0, %xmm2
	testb	$1, %sil
	je	.L17
	andq	$-2, %rsi
	addq	%rsi, %rcx
.L20:
	movq	(%rdi,%rcx,8), %xmm0
	paddq	%xmm0, %xmm2
.L17:
	paddq	%xmm1, %xmm2
	movq	%xmm2, %rax
	ret
.L32:
	pxor	%xmm1, %xmm1
	xorl	%ecx, %ecx
	movdqa	%xmm1, %xmm2
	jmp	.L19
	.cfi_endproc
.LFE16:
	.size	sum_four, .-sum_four
	.ident	"GCC: (Debian 14.2.0-19) 14.2.0"
	.section	.note.GNU-stack,"",@progbits
