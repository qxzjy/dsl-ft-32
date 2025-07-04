import torch.nn as nn

class RecommendationModel(nn.Module):
    def __init__(self, num_users, num_items, latent_dim=10):
        super(RecommendationModel, self).__init__()
        self.user_embedding = nn.Embedding(num_users, latent_dim)
        self.item_embedding = nn.Embedding(num_items, latent_dim)
    
    def forward(self, user, item):
        user_vector = self.user_embedding(user)
        item_vector = self.item_embedding(item)
        return (user_vector * item_vector).sum(1)
