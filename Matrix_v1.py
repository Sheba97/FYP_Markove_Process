import numpy as np

class Matrix:
    def __init__(self, failure_rates, repair_rates, num_sections):
        self.failure_rates = np.array(failure_rates)
        self.repair_rates = np.array(repair_rates)
        self.num_sections = num_sections
        self.mat_size = 2 * (2 ** num_sections - 1)
        self.transition_matrix = None

    def create_matrix(self):
        s_rate = 8760  # Default switching rate (per year)

        # Initialize transition matrix
        trans_mat = np.zeros((self.mat_size, self.mat_size))

        # First column setup
        trans_mat[0, :] = 1  # First row is all ones

        # Fill the first column (index 0) from second row onwards
        for i in range(1, self.mat_size):
            if i % 2 == 1:
                trans_mat[i, 0] = self.failure_rates[i // 2]
            else:
                trans_mat[i, 0] = 0

        # Build the rest of the transition matrix
        for i in range(1, self.mat_size):
            if i % 2 == 1:
                trans_mat[i, i] = -s_rate
                trans_mat[i, i + 1] = s_rate if i + 1 < self.mat_size else 0
            else:
                idx = (i - 1) // 2
                trans_mat[i, i] = -self.repair_rates[idx]
                if i + 1 < self.mat_size:
                    trans_mat[i, i + 1] = self.repair_rates[idx]

        self.transition_matrix = trans_mat
        return self.transition_matrix

    def matrix_calling(self):
        if self.transition_matrix is None:
            raise ValueError("Transition matrix not created. Call create_matrix() first.")

        # Right-hand side vector (only first element is 1)
        b = np.zeros((self.mat_size, 1))
        b[0, 0] = 1

        # Solve the linear system Ax = b
        try:
            result = np.linalg.solve(self.transition_matrix, b)
        except np.linalg.LinAlgError:
            raise ValueError("Transition matrix is singular and cannot be inverted.")
        return result
