import numpy as np
import torch
from .strategy import Strategy

class MarginSamplingDropout(Strategy):
	def __init__(self, X, Y, idxs_lb, args, n_drop=100):
		super(MarginSamplingDropout, self).__init__(X, Y, idxs_lb, args)
		self.n_drop = n_drop

	def query(self, n):
		idxs_unlabed = np.arange(self.n_pool)[~self.idxs_lb]
		probs = self.predict_prob_dropout(self.X[idxs_unlabed], self.Y[idxs_unlabed], self.n_drop)
		probs_sorted, idxs = probs.sort(descending=True)
		U = probs_sorted[:, 0] - probs_sorted[:,1]
		return idxs_unlabed[U.sort()[1][:n]]
