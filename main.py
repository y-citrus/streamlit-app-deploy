    # リストから偶数だけを抽出する関数  
def extract_even_numbers(numbers):
    even_numbers = []
    for number in numbers:
        if number % 2 == 0:
            even_numbers.append(number)
    return even_numbers

# 関数「extract_even_numbers」に要素数が10のリストを渡して、戻り値のリストの合計値と平均値を計算して表示する
numbers = list(range(10))

even_numbers = extract_even_numbers(numbers)

total = sum(even_numbers)
average = total / len(even_numbers) if even_numbers else 0
print("Even Numbers:", even_numbers)
print("Total of Even Numbers:", total)
print("Average of Even Numbers:", average)

# 数値のリストを受け取り、各値に基づいてカテゴリを分類する関数を作成してください

# 条件:

# 1. 値が0以下の場合は "Low" カテゴリに分類してください

# 2. 値が1以上10以下の場合は "Medium" カテゴリに分類してください

# 3. 値が10を超える場合は "High" カテゴリに分類してください

# 4. 入力リストには整数が含まれるものとします

# 結果を辞書形式で返してください。キーがカテゴリ名で、値が該当する数値のリストとします
def categorize_numbers(numbers):
    categories = {
        "Low": [],
        "Medium": [],
        "High": []
    }
    for number in numbers:
        if number <= 0:
            categories["Low"].append(number)
        elif 1 <= number <= 10:
            categories["Medium"].append(number)
        else:
            categories["High"].append(number)
    return categories       

def calculate_bmi(weight, height):
    if height <= 0:
        return "Invalid height"
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
    else:
        category = "Obesity"
    return bmi, category        


# BMIを計算する関数

# BMIを表示してから戻り値を返す

def calculate_bmi_and_display(weight, height):
    bmi, category = calculate_bmi(weight, height)
    print(f"BMI: {bmi:.2f}, Category: {category}")
    return bmi, category        

