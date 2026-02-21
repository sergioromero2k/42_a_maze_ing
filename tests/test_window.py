from mlx import Mlx


def main() -> None:
    # 1. Instantiate the class
    m = Mlx()

    # 2. Initialize the connection (mandatory in this version)
    # This returns the mlx_ptr that the library needs for everything
    mlx_ptr = m.mlx_init()

    # 3. Create the window
    # Pass mlx_ptr as the first argument
    win_ptr = m.mlx_new_window(mlx_ptr, 400, 400, "Test MLX - 42 Madrid")

    # 4. Draw the red square
    # It also requires mlx_ptr and then win_ptr
    for x in range(100, 300):
        for y in range(100, 150):
            m.mlx_pixel_put(mlx_ptr, win_ptr, x, y, 0xFF0000)

    print("Window opened successfully!")
    print("To exit: Close the window or press Ctrl+C in the terminal.")

    # 5. Enter the main loop
    m.mlx_loop(mlx_ptr)


if __name__ == "__main__":
    main()
