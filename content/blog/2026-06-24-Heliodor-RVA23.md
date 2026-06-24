+++
title = "Heliodor: An RVA23-Compliant Multicore Out-of-Order RISC-V Core in Veryl"
+++

[Heliodor](https://github.com/dalance/heliodor) is a from-scratch multicore
out-of-order RISC-V core written in Veryl. We have been using it as a
real-scale design to drive the Veryl compiler and the
[native Veryl simulator](@/blog/2026-05-26-Veryl-Simulator-Performance.md).
This post announces a milestone: with the addition of the vector (V)
extension Heliodor is now compliant with the full RVA23
profile, and runs a vector-enabled Linux kernel with
userspace vector code on top of it. It also passes the official RISC-V
Architectural Compatibility Tests (ACT) v4 — not just for the base RV64GC,
but across the broad set of RVA23 extensions that ACT v4 covers.

## Design

Heliodor is a 2-wide superscalar out-of-order RV64 core. It performs
register renaming onto a physical register file (RAT + free list, with a
64-entry integer PRF and 64-entry FP PRF), uses Tomasulo-style dynamic
scheduling, and commits in order through a 32-entry reorder buffer for
precise exceptions. Branch prediction combines a BTB, a
gshare BHT, a TAGE-lite direction predictor, an indirect-target BTB, and a
return-address stack, with execute-time early redirect on mispredicts. The
memory pipeline does memory-dependence speculation with commit-time replay,
store-to-load forwarding from in-flight and committed stores, and a
write-combining committed-store buffer.

It runs as 1 / 2 / 4 / 8-hart SMP. Each hart has private write-back L1
caches (16 KB, 4-way, non-blocking with MSHRs and critical-word-first fill)
kept coherent through a shared 128 KB L2 with an inclusive MESI directory
and cache-to-cache transfer; AMO / LR-SC stay in cache and the instruction
side is coherent, so `FENCE.I` and `SFENCE.VMA` need no flush sweep. The
shared bus is a split-transaction read controller with modeled DRAM latency.

The ISA is the full RVA23 profile — RVA23S64, the supervisor-mode profile
for 64-bit application processors, which subsumes the RVA23U64 user
profile: RV64GC plus Zba/Zbb/Zbs, Zacas/Zabha atomics, Zfa, Zfhmin, Sstc, Svnapot,
Svpbmt, Svadu, Zicbom/Zicboz, Zicond, Zawrs, Svinval, Zkt, Sscofpmf,
Supm/Ssnpm, PMP (Smpmp), Sv39 virtual memory at M / S / U, the hypervisor
(H) extension that RVA23S64 mandates, and the just-added vector (V)
extension — the last RVA23 piece to land.

The H-extension support spans the HS / VS / VU modes, two-stage
Sv39 × Sv39x4 translation cached in a VMID/VS-ASID-tagged TLB,
`HLV`/`HLVX`/`HSV`, the guest-page-fault trio, virtual-interrupt delivery,
and Sstc-in-VS guest timers.

The vector unit (RVV 1.0) is a decoupled, in-order unit beside the
out-of-order scalar core: it owns the 32 × 128-bit vector register file
(VLEN = 128, ELEN = 64) and the vector CSRs, and runs vector ops in program
order rather than renaming them into the scalar out-of-order machinery. It
covers integer and single/double FP at all LMUL, the full range of vector
loads/stores, masking, and widening/narrowing. Vector state plugs into the
standard `mstatus.VS` / `sstatus.VS` / `vsstatus.VS` controls and the same
two-stage translation as the rest of the H extension, so it works across all
of M / HS / VS / VU.

## Verification

Heliodor's scalar RVA23 ISA is machine-checked against the official RISC-V
Architectural Compatibility Tests (ACT) v4 — the conformance suite whose
expected results are signed by the formal RISC-V Sail golden model —
passing 506 / 506 across integer / atomic (incl. Zacas / Zabha) / FP /
compressed / CSR / Zb* / Zc* / Zfa / Zfhmin / Zicbo* / PMP / Sv* /
exceptions. It also runs the `riscv-tests` arch suites, the in-tree directed
tests for OoO, memory coherence, and H-extension corners, and an RVWMO
litmus harness.

ACT v4 has no vector suite (nor one for the hypervisor extension), so those
two are validated separately. The vector unit is checked by Heliodor's
in-tree RVV arch suites, then exercised end-to-end by booting a V-aware
Linux 7.1 kernel that discovers the vector extension and runs vector code.
Heliodor boots mainline Linux 5.15 / 6.6 LTS / 7.1 SMP through OpenSBI to
SBI shutdown on 1 / 2 / 4 (and 5.15 on 8) harts — the 7.1 boot also drives
userspace floating point across SMP context switches — and a self-written
bare-metal type-1 hypervisor boots an unmodified guest Linux to its own
userspace using the H extension. The boots are cross-checked on Verilator
and a second Veryl simulator backend.

Here is the full boot log — the `[HV]` lines are the type-1
hypervisor, and everything between them is an unmodified guest Linux 7.1
(`Machine model: Heliodor guest`) running on the virtualized HS / VS / VU
modes, from hypervisor start through the guest discovering Sstc-in-VS, its
own init, and SBI shutdown:

<style>
.content .hv-log pre,
.content .hv-log code { line-height: 1.15; }
</style>

<div class="hv-log" style="font-size: 0.7em;">

```text
[HV] hypervisor up on heliodor H-extension
[HV] entering guest at 0x0000000080200000
Booting Linux on hartid 0
Linux version 7.1.0 (builder@host) (riscv64-unknown-elf-gcc (g04696df0963) 14.2.0, GNU ld (GNU Binutils) 2.43.1) #8 SMP PREEMPT Tue Jun 16 15:02:43 JST 2026
Machine model: Heliodor guest
SBI specification v1.0 detected
SBI implementation ID=0x0 Version=0x0
SBI TIME extension detected
SBI IPI extension detected
SBI RFENCE extension detected
SBI SRST extension detected
earlycon: sbi0 at I/O port 0x0 (options '')
printk: legacy bootconsole [sbi0] enabled
Disabled 4-level and 5-level paging
efi: UEFI not found.
OF: reserved mem: Reserved memory: No reserved-memory node in the DT
SBI HSM extension detected
riscv: base ISA extensions acdfim
riscv: ELF capabilities acdfim
Ticket spinlock: enabled
Zone ranges:
  DMA32    [mem 0x0000000080000000-0x0000000081bfffff]
  Normal   empty
Movable zone start for each node
Early memory node ranges
  node   0: [mem 0x0000000080000000-0x0000000081bfffff]
Initmem setup node 0 [mem 0x0000000080000000-0x0000000081bfffff]
percpu: Embedded 12 pages/cpu s18648 r0 d30504 u49152
Kernel command line: earlycon=sbi no4lvl nokaslr
Unknown kernel command line parameters "nokaslr", will be passed to user space.
printk: log buffer data + meta data: 131072 + 458752 = 589824 bytes
Dentry cache hash table entries: 4096 (order: 3, 32768 bytes, linear)
Inode-cache hash table entries: 2048 (order: 2, 16384 bytes, linear)
software IO TLB: SWIOTLB bounce buffer size adjusted to 0MB
software IO TLB: area num 1.
software IO TLB: mapped [mem 0x0000000081b32000-0x0000000081b72000] (0MB)
Built 1 zonelists, mobility grouping on.  Total pages: 7168
mem auto-init: stack:all(zero), heap alloc:off, heap free:off
SLUB: HWalign=64, Order=0-1, MinObjects=0, CPUs=1, Nodes=1
rcu: Hierarchical RCU implementation.
rcu: 	RCU restricting CPUs from NR_CPUS=8 to nr_cpu_ids=1.
rcu: RCU calculated value of scheduler-enlistment delay is 25 jiffies.
rcu: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=1
NR_IRQS: 64, nr_irqs: 64, preallocated irqs: 0
riscv-intc: 64 local interrupts mapped
riscv: providing IPIs using SBI IPI extension
rcu: srcu_init: Setting srcu_struct sizes based on contention.
clocksource: riscv_clocksource: mask: 0xffffffffffffffff max_cycles: 0x24e6a1710, max_idle_ns: 440795202120 ns
sched_clock: 64 bits at 10MHz, resolution 100ns, wraps every 4398046511100ns
riscv-timer: Timer interrupt in S-mode is available via sstc extension
Calibrating delay loop (skipped), value calculated using timer frequency.. 20.00 BogoMIPS (lpj=40000)
pid_max: default: 32768 minimum: 301
Mount-cache hash table entries: 512 (order: 0, 4096 bytes, linear)
Mountpoint-cache hash table entries: 512 (order: 0, 4096 bytes, linear)
VFS: Finished mounting rootfs on nullfs
ASID allocator using 16 bits (65536 entries)
rcu: Hierarchical SRCU implementation.
rcu: 	Max phase no-delay instances is 1000.
EFI services will not be available.
smp: Bringing up secondary CPUs ...
smp: Brought up 1 node, 1 CPU
Memory: 24968K/28672K available (894K kernel code, 542K rwdata, 147K rodata, 241K init, 214K bss, 2876K reserved, 0K cma-reserved)
clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 7645041785100000 ns
DMA: preallocated 128 KiB GFP_KERNEL|GFP_DMA32 pool for atomic allocations
clocksource: Switched to clocksource riscv_clocksource
workingset: timestamp_bits=62 (anon: 58) max_order=13 bucket_order=0 (anon: 0)
clk: Disabling unused clocks
Warning: unable to open an initial console.
Freeing unused kernel image (initmem) memory: 240K
Kernel memory protection not selected by kernel config.
Run /init as init process
reboot: Power down
[HV] guest issued SBI system_reset (shutdown)
H5.2b SoC hypervisor guest boot: cy=014662b0 x3=00000000000000aa pass=1
```

</div>

## Why Heliodor exists

Heliodor is not a product. Its purpose is to be a large, realistic stress
test for the Veryl toolchain: a design big enough that compile time,
analyzer scaling, error messages, simulator performance, and waveform
ergonomics all matter, and complex enough that bugs in the toolchain
actually show up. The
[Veryl simulator performance numbers](@/blog/2026-05-26-Veryl-Simulator-Performance.md)
already on this blog — measured against Verilator on a full Linux boot —
came out of using Heliodor as exactly that workload. Its size likewise
exercises the [IR-based analyzer](@/blog/2026-01-20-IR-Based-Analysis.md):
we routinely check that analysis still scales to a design this large, and
Heliodor has surfaced order-of-magnitude performance regressions that
smaller test cases never hit.

Reaching full RVA23 compliance means Heliodor can now stand in for a modern
application-class RISC-V core when we benchmark, profile, and debug Veryl
itself.

## Acknowledgement

Heliodor is developed almost entirely through
[Claude Code](https://www.anthropic.com/claude-code) — the RTL itself, the
debugging, the directed tests, and the bring-up of each ISA extension. The
API tokens that made this possible are provided by Anthropic's
[Claude for Open Source](https://claude.com/contact-sales/claude-for-oss)
program, which supports open-source projects that build with Claude. Thanks
to the program, Heliodor has been able to scale from an RV64I scalar
pipeline to a multi-hart, RVA23-compliant out-of-order core that boots
mainline Linux, in a timeframe that would otherwise have been out of reach
for a hobby project. We are grateful for the support.
