# Wavetrap

An GnuRadio IQ Recorder.

## Installation

```bash
cd gr-wavetrap
mkdir build
cd build
cmake ../
make -j4
sudo make install
sudo ldconfig
```


## Sources

The Flowgraph is based on [wavetrap by muaddib1984](https://github.com/muaddib1984/wavetrap)

The OOT Block `Head with RST` is taken from [gr-aoa](https://github.com/MarcinWachowiak/gr-aoa) and was extended with a Message in port to trigger the reset.
