from logic import process_orders
import os

def test_process():
    def log(msg):
        print(f"LOG: {msg}")

    def prog(curr, tot):
        print(f"PROGRESS: {curr}/{tot}")

    out_dir = "Generated_Orders"
    success, msg = process_orders(
        template_path="Template.xlsx",
        data_path="Data.xlsx",
        output_dir=out_dir,
        config_path="config.json",
        progress_callback=prog,
        log_callback=log
    )
    print(f"Result: {success}, {msg}")

if __name__ == "__main__":
    test_process()
