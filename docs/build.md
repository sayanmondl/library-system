# Build

### Clone this repository [https://github.com/sayanmondl/library-system]
```bash
git clone https://github.com/sayanmondl/library-system.git
``` 
### Change Directory
```bash
cd library-system
```

<details>
<summary style="font-size: medium;">Linux</summary>

### Install miniconda  (Optional)
```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```
### Create environment and activate (Optional)
```bash
conda create --name libenv python=3.10
conda activate libenv
```

### Install Requirements

```bash
pip3 install -r requirements.txt
``` 

</details>


<details>
<summary style="font-size: medium;">Windows</summary>

### Install miniconda  (Optional)
```bash
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
start /wait "" miniconda.exe /S
del miniconda.exe
```
### Create environment and activate (Optional)
#### Open Anaconda prompt, then:
```bash
conda create --name libenv python=3.10
conda activate libenv
```

### Install Requirements
```bash
pip install -r requirements.txt
``` 

</details>

### Run the Python file
#### In Linux:
- To run this in a standalone teminal we have to first source the .env file

    ```bash
    source .env
    ```
- Then:
    ```bash
    cd source
    python3 main.py
    ```
#### In Windows:
- To run this in a standalone terminal we have to update environment variables

    ```powershell
    Get-Content .env | ForEach-Object {
        $name, $value = $_ -split '=', 2
        [System.Environment]::SetEnvironmentVariable($name, $value)
    }
    ```
- Then:
    ```bash
    cd source
    python main.py
    ```