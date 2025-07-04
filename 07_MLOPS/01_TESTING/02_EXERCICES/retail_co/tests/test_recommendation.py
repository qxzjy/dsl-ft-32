from app.recommendation import recommend
from app.model import RecommendationModel

def test_recommend():
    model = RecommendationModel(num_users=3, num_items=3)
    recommended_items = recommend(model, user_id=0, num_users=3, num_items=3, top_n=2)
    assert len(recommended_items) == 2
    assert all(0 <= item < 3 for item in recommended_items)
