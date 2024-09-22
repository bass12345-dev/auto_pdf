import redis
import time
from progress.bar import Bar

# Set up Redis connection
r = redis.Redis(host='localhost', port=6380, db=0)

def task_with_progress(task_id, total_steps):
    # Initialize Redis with starting progress (0%)
    r.set(f'progress:{task_id}', 0)

    # Create a progress bar
    bar = Bar('Processing', max=total_steps)
    
    for i in range(total_steps):
        # Simulate work by sleeping
        time.sleep(0.1)
        
        # Update progress in Redis (in percentage)
        progress = int((i + 1) / total_steps * 100)
        r.set(f'progress:{task_id}', progress)

        # Update the progress bar in the console
        bar.next()
    
    bar.finish()
    print("Task Completed")

if __name__ == "__main__":
    # Simulate task with 100 steps
    task_with_progress("task_1", 100)
