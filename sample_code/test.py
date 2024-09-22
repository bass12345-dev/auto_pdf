
def loop():
    inner_counter = 0
        # Outer loop
    for i in range(3):
        # Code outside inner loop
        print(f"Outer loop, iteration {i}: code outside inner loop")

        # Inner loop
        for j in range(5):
            inner_counter += 1  # Increment the continuing counter
            print(f"  Inner loop, iteration {inner_counter}: code inside inner loop")
        
        # Code after inner loop
        print(f"Outer loop, iteration {i}: code after inner loop\n")

  
if __name__ == '__main__':
    loop()
