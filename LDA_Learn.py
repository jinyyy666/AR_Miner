import numpy as np
import lda
model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
model.fit(X)
