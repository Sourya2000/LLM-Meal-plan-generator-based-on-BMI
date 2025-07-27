# LLM Mean plan generator based on BMI

## Basic setup

``` bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

* Create `dataset` folder in the main path and copy the `epi_r.csv`

``` bash
# Generate mean_plan dataset
python -m src.scripts.dataset

# Create a new file called .env and add:
DATASET_DIR="path_to_folder/hcai/dataset"
DAYS_COUNT=30

# Run UI
python -m streamlit run src/main.py

# Run UI without opening in browser
python -m streamlit run src/main.py --server.headless true

# Run only the llm code without UI
python -m src.main_llm

```

## Files

* Dataset: [Epi Recipes](https://www.kaggle.com/datasets/hugodarwood/epirecipes?resource=download)
* dataset.py: preprocessing of epi_r.csv and gives meal_dataset.csv
* meal_generation.py: Rag - ⚠️ IGNORE
* meal_generation.py_rag_LLM.py: Rag and LLM
* meal_generation_calorie.py: calorie, fat, protein and sodium
* vectorstore_builder.py: vector embedding and retrieval

![image alt](https://github.com/Sourya2000/LLM-Meal-plan-generator-based-on-BMI/blob/main/Screenshot%202025-07-27%20020019.png?raw=true)
![image alt](https://github.com/Sourya2000/LLM-Meal-plan-generator-based-on-BMI/blob/main/Screenshot%202025-07-27%20020131.png?raw=true)

