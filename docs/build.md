# Build

### Clone this repository [https://github.com/sayanmondl/library-system]
```shell
git clone https://github.com/sayanmondl/library-system.git
``` 
### Change Directory
```shell
cd library-system
```

<details>
<summary style="font-size: medium;">Linux</summary>

### Install miniconda  (Optional)
```shell
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```
### Create environment and activate (Optional)
```shell
conda create --name libenv python=3.10
conda activate libenv
```

### Install Requirements

```shell
pip3 install -r requirements.txt
``` 

</details>


<details>
<summary style="font-size: medium;">Windows</summary>

### Install miniconda  (Optional)
```shell
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
start /wait "" miniconda.exe /S
del miniconda.exe
```
### Create environment and activate (Optional)
#### Open Anaconda prompt, then:
```shell
conda create --name libenv python=3.10
conda activate libenv
```

### Install Requirements
```shell
pip install -r requirements.txt
``` 

</details>

### Run the Python file
#### In Linux:
```shell
cd source
python3 main.py
```
#### In Windows:
```shell
cd source
python main.py
```