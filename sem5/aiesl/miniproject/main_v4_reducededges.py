import os
import pandas as pd
import networkx as nx
import math
import glob
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import recall_score
from sklearn.metrics import ndcg_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score
import torch_geometric.utils as utils
# from dgl.nn.pytorch import GATConv
from torch_geometric.utils import softmax
import torch
import torch.nn as nn
import torch.nn.functional as F
import random
import dgl
import uuid
import dgl.nn.pytorch as dglnn
import numpy as np
import torch as th
import torch.optim as optim
import dgl.function as fn
from dgl.nn import GraphConv
from sklearn.metrics import roc_auc_score, ndcg_score, recall_score
from torch_geometric.data import Data
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import add_self_loops, degree
from torch.utils.data import Dataset, DataLoader
import torch.nn.utils.rnn as rnn_utils
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
import zipfile
from sklearn.metrics import ndcg_score, recall_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
import logging
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.preprocessing import label_binarize
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import StratifiedShuffleSplit

# --- START FIX 1: NEW IMPORTS ---
import faiss  # For efficient similarity search
from sklearn.preprocessing import normalize # For L2 normalization
# --- END FIX 1 ---


# Configure the logging system
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')

# Now you can use logging to write log messages
logging.info('This is an informational log message.')

folder_path = r"/home/ibu/Food/Food"
files_to_read = ['Food_Dataset.zip']
file_path = r"/home/ibu/Food/Food_Dataset.zip"

# Read the file into a pandas DataFrame
# Adding error handling for file reading
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    logging.error(f"Error: File not found at {file_path}")
    exit()
except Exception as e:
    logging.error(f"Error reading CSV file: {e}")
    exit()

def process_data(df_to_process):
    """Processes the DataFrame to print dataset statistics."""
    logging.info("Processing data statistics...")
    # Create a dictionary to store recipe_id as key and total score and count as values
    recipe_scores = {}

    # Iterate through user_id, recipe_id, and rating columns to calculate total score and count for each recipe_id
    for i in range(len(df_to_process)):
        # Use .iloc for robust row access
        rid = df_to_process.iloc[i]['recipe_id']
        r = df_to_process.iloc[i]['rating']
        if rid not in recipe_scores:
            recipe_scores[rid] = {'total_score': 0, 'count': 0}
        recipe_scores[rid]['total_score'] += r
        recipe_scores[rid]['count'] += 1

    # Count the number of unique user_ids
    num_unique_user_ids = df_to_process['user_id'].nunique()
    # Count the number of unique recipe_ids
    num_unique_recipe_ids = df_to_process['recipe_id'].nunique()
    # Count the number of unique ingredients
    num_unique_ingredients = df_to_process['ingredients'].nunique()
    # Count the number of unique combinations of user_id and recipe_id
    num_interactions = df_to_process[['user_id', 'recipe_id']].drop_duplicates().shape[0]
    
    # Avoid division by zero if dataset is empty
    if num_unique_user_ids == 0 or num_unique_recipe_ids == 0:
        sparsity = 0
    else:
        sparsity = (1 - (num_interactions / (num_unique_user_ids * num_unique_recipe_ids))) * 100
       
    # Group the data by 'user_id' and count the number of unique 'recipe_id' each user has rated
    user_rating_counts = df_to_process.groupby('user_id')['recipe_id'].nunique()

    # Now, you can create a histogram based on the number of users who have rated a certain number of items
    user_count_histogram = user_rating_counts.value_counts().sort_index()

    
    # Print the counts
    print(f"Number of unique user_ids: {num_unique_user_ids}")
    print(f"Number of unique recipe_ids: {num_unique_recipe_ids}")
    print(f"Number of interactions between users and recipes: {num_interactions}")
    print(f"Number of unique ingredients: {num_unique_ingredients}")
    print("************************************")
    print(f"Sparsity of the dataset: {sparsity:.2f}%")
    print("************************************")
    print("Number of Users per Rating Count:")
    for count, users in user_count_histogram.items():
        print(f" [{count}] {users} users have {count} rated recipes")
    print("************************************")

def Load_Into_Graph(df):
    """Given a data frame with columns 'user_id', 'recipe_id',
    'ingredients', and 'nutrition', construct a multigraph.
    """
    logging.info("Loading data into a graph...")
    
    # Create an empty graph
    G = nx.Graph()

    nutrients = ["Proteins", "Carbohydrates", "Sugars",
                "Sodium", "Fat", "Saturated_fats", "Fibers"]
    G.add_nodes_from(nutrients, node_type='nutrition')

    # Iterate through the data and populate the graph
    for uid, rid, r, ing, nut in df[['user_id', 'recipe_id', 'rating', 'ingredients', 'nutrition']].itertuples(False, None):
        # Add user_id, recipe_id
        G.add_node(f"u{uid}", node_type='user')
        G.add_node(f"r{rid}", node_type='recipe')

        # Add edges between user_id and recipe_id
        G.add_edge(f"u{uid}", f"r{rid}", weight=r, edge_type='rating')

        # Add new ingredients as nodes
        if type(ing) is str:
            try:
                # Remove brackets and single quotes
                ing = eval(ing)
                G.add_nodes_from(ing, node_type='ingredients')
                # Add edges between recipe_id and ingredients
                for i in ing: 
                    G.add_edge(f"r{rid}", i, edge_type='ingredient')
            except Exception as e:
                logging.warning(f"Could not eval ingredients: {ing}. Error: {e}")

        # Add edges between recipe_id and nutrients
        if type(nut) is str:
            try:
                nuts = eval(nut)
                for j, nut_name in enumerate(nutrients):
                    if j < len(nuts) and nuts[j] > 0:
                        G.add_edge(f"r{rid}", nut_name, weight=nuts[j], edge_type='nutrition')
            except Exception as e:
                 logging.warning(f"Could not eval nutrition: {nut}. Error: {e}")

    logging.info("Finished; resulting graph:")
    logging.info(G)
    return G

def Heterogeneous_Graph(df):
    # Populate the heterogeneous graph
    G = Load_Into_Graph(df)

    # Define the meta-paths
    meta_paths = [
        ['user_id', 'recipe_id', 'nutrition', 'ingredients'],
        ['user_id', 'recipe_id'],
        ['user_id', 'recipe_id', 'ingredients', 'nutrition'],
        ['recipe_id', 'nutrition', 'ingredients'],
        ['recipe_id', 'ingredients', 'nutrition']
    ]

    # Print the edges and their attributes for each meta-path
    for meta_path in meta_paths:
        # logging.info("Meta-Path: %s", " -> ".join(meta_path))
        paths = []

        # Check if the meta-path starts with 'user_id' and ends with 'ingredients'
        if meta_path[0] == 'user_id' and meta_path[-1] == 'ingredients':
            for uid in G.nodes():
                if G.nodes[uid]['node_type'] == 'user':
                    for rid in G.neighbors(uid):
                        if G.nodes[rid]['node_type'] == 'recipe':
                            for ing in G.neighbors(rid):
                                if G.nodes[ing]['node_type'] == 'ingredients':
                                    paths.append([f"{uid}", f"{rid}", ing])

        # Check if the meta-path starts with 'user_id' and ends with 'nutrition'
        elif meta_path[0] == 'user_id' and meta_path[-1] == 'nutrition':
            for uid in G.nodes():
                if G.nodes[uid]['node_type'] == 'user':
                    for rid in G.neighbors(uid):
                        if G.nodes[rid]['node_type'] == 'recipe':
                            for nut in G.neighbors(rid):
                                if G.nodes[nut]['node_type'] == 'nutrition':
                                    for ing in G.neighbors(rid):
                                        if G.nodes[ing]['node_type'] == 'ingredients':
                                            paths.append([f"{uid}", f"{rid}", nut, ing])
        # ... (logging code is commented out, so leaving as is) ...


# Define the NLA class
class NLA(nn.Module):
    def __init__(self, num_users, num_recipes, num_ingredients, num_nutrition, embedding_dim, paths):
        super(NLA, self).__init__()

        # Embedding layers
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.recipe_embedding = nn.Embedding(num_recipes, embedding_dim)
        self.ingredient_embedding = nn.Embedding(num_ingredients, embedding_dim)
        self.nutrition_embedding = nn.Embedding(num_nutrition, embedding_dim)

        # Convert the paths to tensors
        self.paths = paths.clone().detach() if paths is not None else None

    def forward(self, uid, rid, ing, nut):
        user_emb = self.user_embedding(uid)
        recipe_emb = self.recipe_embedding(rid)
        ingredient_emb = self.ingredient_embedding(ing)
        nutrition_emb = self.nutrition_embedding(nut)

        if self.paths is not None:
            # Node-Level Attention
            weighted_attention = user_emb.unsqueeze(1) / user_emb.size(1)
            aggregated_attention = torch.sum(weighted_attention, dim=1)

            max_size = max(user_emb.size(0), recipe_emb.size(0), aggregated_attention.size(0))

            user_emb = F.pad(user_emb, (0, 0, 0, max_size - user_emb.size(0)))
            recipe_emb = F.pad(recipe_emb, (0, 0, 0, max_size - recipe_emb.size(0)))
            aggregated_attention = F.pad(aggregated_attention, (0, 0, 0, max_size - aggregated_attention.size(0)))

            node_embeddings = torch.cat((user_emb, recipe_emb, aggregated_attention), dim=1)
        else:
            node_embeddings = torch.cat((user_emb, recipe_emb, ingredient_emb, nutrition_emb), dim=1)

        return node_embeddings

    def train_nla(self, df, user_encoder, recipe_encoder, ingredient_encoder, nutrition_encoder, num_epochs):
        criterion_nla = nn.MSELoss()
        optimizer_nla = optim.Adam(self.parameters(), lr=0.01)

        dataset = HeterogeneousDataset(df, user_encoder, recipe_encoder, ingredient_encoder, nutrition_encoder)
        data_loader = DataLoader(dataset, batch_size=32, shuffle=True)

        for epoch in range(num_epochs):
            running_loss_nla = 0.0
            for uid, rid, ing, nut, label in data_loader:
                optimizer_nla.zero_grad()
                embeddings = self(uid, rid, ing, nut)
                label = label.unsqueeze(1).float()
                label = label.repeat(1, embeddings.size(1))
                loss_nla = criterion_nla(embeddings, label)
                running_loss_nla += loss_nla.item()
                loss_nla.backward()
                optimizer_nla.step()

            avg_loss_nla = running_loss_nla / len(data_loader)
            logging.info(f"Epoch {epoch + 1}/{num_epochs}, NLA Loss: {avg_loss_nla:.4f}")
        
        return avg_loss_nla

    def get_embeddings(self, uid, rid, ing, nut):
        with torch.no_grad():
            embeddings = self(uid, rid, ing, nut)
        return embeddings
    
# Define the dataset class
class HeterogeneousDataset(Dataset):
    def __init__(self, df, user_encoder, recipe_encoder, ingredient_encoder, nutrition_encoder):
        self.uids = user_encoder.transform(df['user_id'])
        self.rids = recipe_encoder.transform(df['recipe_id'])
        self.ings = ingredient_encoder.transform(df['ingredients'])
        self.nuts = nutrition_encoder.transform(df['nutrition'])
        self.labels = df['rating'].astype(float).values

    def __len__(self):
        return len(self.uids)

    def __getitem__(self, idx):
        uid = self.uids[idx]
        rid = self.rids[idx]
        ing = self.ings[idx]
        nut = self.nuts[idx]
        label = self.labels[idx]
        return uid, rid, ing, nut, label

def find_paths_users_interests(df):
    # This still builds the giant graph, which is memory-intensive
    # but the path list is the part causing the 30GB crash.
    G = Load_Into_Graph(df)

    avg_rating_map = df.groupby('recipe_id')['rating'].mean()
    df['avg_rating'] = df['recipe_id'].map(avg_rating_map)
    meta_path = ['user_id', 'recipe_id', 'ingredient', 'nutrition']
    
    paths = []
    
    # --- START FIX: ADDING A PATH LIMIT ---
    # Set a hard limit on the number of paths to generate.
    # 5 million paths is large but should be manageable in RAM.
    # If 30GB is still used, lower this to 1,000,000.
    TOTAL_PATH_LIMIT = 5_000_000 
    # --- END FIX ---

    logging.info("Starting path generation in find_paths_users_interests...")
    
    # We must break out of all nested loops once the limit is hit
    try:
        for uid in G.nodes():
            if G.nodes[uid]['node_type'] == 'user':
                user_rated_recipes = [rid for rid in G.neighbors(uid) if G.nodes[rid]['node_type'] == 'recipe']
                for rid in user_rated_recipes:
                    try:
                        recipe_id_numeric = int(rid[1:]) 
                        matching_rows = df[df['recipe_id'] == recipe_id_numeric]
                    except ValueError:
                        continue
                    
                    if not matching_rows.empty:
                        # Check if 'avg_rating' exists, handle missing values
                        avg_rating = matching_rows['avg_rating'].iloc[0]
                        if pd.isna(avg_rating):
                            continue # Skip if no avg_rating was calculated
                            
                        if matching_rows['rating'].iloc[0] >= avg_rating:
                            ingredient_node = []
                            nutrition_node = []

                            for node in G.neighbors(rid):
                                if G.nodes[node]['node_type'] == 'ingredients':
                                    ingredient_node.append(node)
                                elif G.nodes[node]['node_type'] == 'nutrition':
                                    nutrition_node.append(node)

                            for ing in ingredient_node:
                                for nut in nutrition_node:
                                    paths.append([uid, rid, ing, nut])
                                    
                                    # --- START FIX: CHECK THE LIMIT ---
                                    if len(paths) >= TOTAL_PATH_LIMIT:
                                        # This will be caught by the outer 'except'
                                        raise StopIteration 
                                    # --- END FIX ---
    except StopIteration:
        logging.warning(f"Reached path limit of {TOTAL_PATH_LIMIT}. Stopping path generation.")
    
    # --- END OF LOOP MODIFICATION ---
    
    logging.info(f"Generated {len(paths)} paths.")

    if not paths:
        logging.warning("No paths found for users' interests. Returning empty tensor.")
        return torch.tensor([], dtype=torch.long), meta_path

    # This part will now run on a manageable list
    logging.info("Encoding paths...")
    user_encoder = LabelEncoder()
    recipe_encoder = LabelEncoder()
    ingredient_encoder = LabelEncoder()
    nutrition_encoder = LabelEncoder()
    user_encoder.fit([path[0] for path in paths])
    recipe_encoder.fit([path[1] for path in paths])
    ingredient_encoder.fit([path[2] for path in paths])
    nutrition_encoder.fit([path[3] for path in paths])

    encoded_paths = [[user_encoder.transform([path[0]])[0], recipe_encoder.transform([path[1]])[0], ingredient_encoder.transform([path[2]])[0], nutrition_encoder.transform([path[3]])[0]] for path in paths]
    
    logging.info("Converting paths to tensor...")
    paths_tensor = torch.tensor(encoded_paths, dtype=torch.long).clone().detach()
    
    return paths_tensor, meta_path

class SLA(nn.Module):
    def __init__(self, num_users, num_recipes, num_ingredients, num_nutrition, embedding_dim, paths, is_healthy=False):
        super(SLA, self).__init__()
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.recipe_embedding = nn.Embedding(num_recipes, embedding_dim)
        self.ingredient_embedding = nn.Embedding(num_ingredients, embedding_dim)
        self.nutrition_embedding = nn.Embedding(num_nutrition, embedding_dim)
        
        self.attention = nn.Sequential(
            nn.Linear(embedding_dim, embedding_dim),
            nn.LeakyReLU(negative_slope=0.01),  
        )
        self.is_healthy = is_healthy  
        self.paths = paths.clone().detach() if paths is not None else None

    def calculate_impression_coefficient(self, source_embedding, destination_embedding):
        return torch.matmul(source_embedding, destination_embedding.T)

    def calculate_weight(self, impression_coefficient):
        return torch.sum(F.leaky_relu(impression_coefficient, negative_slope=0.01))

    def forward(self, uid, rid, ing, nut, is_healthy=None):
        if is_healthy is None:
            is_healthy = self.is_healthy
        else:
            is_healthy = F.leaky_relu(is_healthy, negative_slope=0.01)

        user_emb = self.user_embedding(uid)
        recipe_emb = self.recipe_embedding(rid)
        ingredient_emb = self.ingredient_embedding(ing)
        nutrition_emb = self.nutrition_embedding(nut)

        max_size = max(user_emb.size(0), recipe_emb.size(0), ingredient_emb.size(0), nutrition_emb.size(0))

        user_emb = F.pad(user_emb, (0, 0, 0, max_size - user_emb.size(0)))
        recipe_emb = F.pad(recipe_emb, (0, 0, 0, max_size - recipe_emb.size(0)))
        ingredient_emb = F.pad(ingredient_emb, (0, 0, 0, max_size - ingredient_emb.size(0)))
        nutrition_emb = F.pad(nutrition_emb, (0, 0, 0, max_size - nutrition_emb.size(0)))

        node_embeddings = torch.cat((user_emb, recipe_emb, ingredient_emb, nutrition_emb), dim=1)
        impression_coefficient = self.calculate_impression_coefficient(user_emb, recipe_emb)
        softmax_impression_coefficient = F.softmax(impression_coefficient, dim=1)
        weight = self.calculate_weight(softmax_impression_coefficient)

        return node_embeddings, impression_coefficient, weight
    
    def edge_loss(self, weight):
        loss = -torch.log(1 / (1 + torch.exp(weight)))
        return loss.mean()

    def train_sla(self, uid_tensor, rid_tensor, ing_tensor, nut_tensor, num_epochs_sla):
        optimizer_sla = optim.Adam(self.parameters(), lr=0.01)

        for epoch_sla in range(num_epochs_sla):
            optimizer_sla.zero_grad()
            
            try:
                node_embeddings, impression_coefficient, weight = self(uid_tensor, rid_tensor, ing_tensor, nut_tensor)
                loss_sla = self.edge_loss(impression_coefficient)
                loss_sla.backward()
                optimizer_sla.step()
                logging.info(f"Epoch SLA {epoch_sla + 1}/{num_epochs_sla}, SLA Loss: {loss_sla.item():.4f}")
            except RuntimeError as e:
                logging.error(f"Error during SLA training epoch {epoch_sla+1}: {e}")
                logging.error("SLA training failed. This is likely due to mismatched tensor sizes in the forward pass.")
                break 

# Define the is_healthy function
def is_healthy(food_data):
    # Expected order: [Fibers, Fat, Sugar, Sodium, Protein, Saturated_fat, Carbohydrates]
    
    if len(food_data) < 7:
        logging.warning(f"Insufficient nutrition data: {food_data}")
        return False
        
    fibres = food_data[0]
    fat = food_data[1]
    sugar = food_data[2]
    sodium = food_data[3]
    protein = food_data[4]
    saturated_fat = food_data[5]
    carbohydrates = food_data[6]
    
    conditions_met = 0
    
    if fibres > 10: conditions_met += 1
    if 15 <= fat <= 30: conditions_met += 1
    if sugar < 10: conditions_met += 1
    if sodium < 5: conditions_met += 1
    if 10 <= protein <= 15: conditions_met += 1
    if saturated_fat < 10: conditions_met += 1
    if 55 <= carbohydrates <= 75: conditions_met += 1
    
    return conditions_met >= 3

def find_healthy_foods(df):
    G = Load_Into_Graph(df)

    paths = []
    healthy_foods = set()

    for uid in G.nodes():
        if G.nodes[uid]['node_type'] == 'user':
            user_rated_recipes = [rid for rid in G.neighbors(uid) if G.nodes[rid]['node_type'] == 'recipe']
            for rid in user_rated_recipes:
                try:
                    recipe_id_numeric = int(rid[1:])
                except ValueError:
                    continue
                
                matching_rows = df[df['recipe_id'] == recipe_id_numeric]
                
                if not matching_rows.empty:
                    try:
                        nutrition_health = eval(matching_rows['nutrition'].iloc[0])
                        is_healthy_food = is_healthy(nutrition_health)
                        
                        if is_healthy_food:
                            healthy_foods.add(rid)
                            ingredient_node = []
                            nutrition_node = []
                            for node in G.neighbors(rid):
                                if G.nodes[node]['node_type'] == 'ingredients':
                                    ingredient_node.append(node)
                                elif G.nodes[node]['node_type'] == 'nutrition':
                                    nutrition_node.append(node)
                            for ing in ingredient_node:
                                for nut in nutrition_node:
                                    paths.append([uid, rid, ing, nut])
                    except Exception as e:
                        logging.warning(f"Error processing nutrition for recipe {rid}: {e}")

    if not paths:
        logging.warning("No healthy food paths found.")
        return torch.tensor([], dtype=torch.long)

    recipe_encoder = LabelEncoder()
    recipe_encoder.fit(list(healthy_foods))
    encoded_paths = [[path[1]] for path in paths if path[1] in healthy_foods]

    paths_tensor = torch.tensor(encoded_paths, dtype=torch.long)
    
    return paths_tensor

def normalize_summed_embeddings(embeddings_nla):
    embeddings_nla = embeddings_nla.detach().numpy()
    scaler = MinMaxScaler()
    normalized_embeddings = scaler.fit_transform(embeddings_nla)
    return normalized_embeddings

def rate_healthy_recipes_for_user(user_id, df):
    user_data = df[df['user_id'] == user_id]
    user_healthy_recipes = set()
    
    for index, row in user_data.iterrows():
        recipe_id = row['recipe_id']
        try:
            nutrition_health = eval(row['nutrition'])
            if is_healthy(nutrition_health):
                user_healthy_recipes.add(recipe_id)
        except Exception as e:
            logging.warning(f"Could not parse nutrition for recipe {recipe_id} for user {user_id}: {e}")

    return user_healthy_recipes

def load_ground_truth_ratings(files_to_read, folder_path):
    ground_truth_ratings = []

    for file in files_to_read:
        if file == 'Food_Dataset.zip':
            try:
                interactions_df = pd.read_csv(os.path.join(folder_path, file), dtype=str)
                ground_truth_ratings.extend(
                    [
                        (int(row['user_id']), int(row['recipe_id']), int(row['rating']))
                        for _, row in interactions_df.iterrows()
                    ]
                )
            except Exception as e:
                logging.error(f"Error in load_ground_truth_ratings: {e}")

    return ground_truth_ratings

# --- START FIX 2: REPLACING 'Recommendation_healthy_recipes' ---
# The original function created a massive cosine_similarity matrix, causing the crash.
# This new version uses the pre-built 'faiss_index' to find similar users
# efficiently without high RAM usage.
def Recommendation_healthy_recipes(df, faiss_index, normalized_embeddings_l2, unique_user_ids, similarity_threshold, top_n_popular):
    recommendations = {}
    actual_ratings = {}

    logging.info("Running Faiss range search for recommendations...")
    # 1. Search the index for ALL users at once.
    # We ask for all neighbors with a similarity > similarity_threshold.
    # `lims` = array where lims[i] to lims[i+1] is the slice for user 'i'
    # `D` = distances/scores
    # `I` = indices of the neighbors
    lims, D, I = faiss_index.range_search(normalized_embeddings_l2, similarity_threshold)
    logging.info("Faiss search complete.")

    num_users = len(unique_user_ids)
    for i in range(num_users):
        user_id = unique_user_ids[i]

        # 2. Get the results for user 'i' from the search
        start_idx = lims[i]
        end_idx = lims[i+1]
        neighbor_indices = I[start_idx:end_idx]

        # 3. Filter out the user itself (whose index is 'i')
        similar_users_indices = [idx for idx in neighbor_indices if idx != i]

        # 4. Collect recipes from these similar users (same logic as before)
        similar_user_rated_recipes = set()
        for similar_user_index in similar_users_indices:
            similar_user_id = unique_user_ids[similar_user_index]
            similar_user_rated_recipes.update(df[df['user_id'] == similar_user_id]['recipe_id'])

        # 5. Calculate popularity and get top N (same logic as before)
        recipe_popularity = {}
        for recipe_id in similar_user_rated_recipes:
            recipe_popularity[recipe_id] = len(df[df['recipe_id'] == recipe_id])

        popular_recipes = sorted(recipe_popularity.items(), key=lambda x: x[1], reverse=True)[:top_n_popular]
        recommended_recipes = {recipe_id: popularity for recipe_id, popularity in popular_recipes}

        recommendations[user_id] = recommended_recipes
        actual_ratings[user_id] = {recipe_id: rating for recipe_id, rating in zip(df[df['user_id'] == user_id]['recipe_id'], df[df['user_id'] == user_id]['rating'])}

    return recommendations, actual_ratings
# --- END FIX 2 ---

def calculate_ndcg(df, user_id, recommendations, k):
    user_ratings = df[(df['user_id'] == user_id) & df['recipe_id'].isin(recommendations)][['recipe_id', 'rating']]
    ratings_dict = dict(zip(user_ratings['recipe_id'], user_ratings['rating']))
    recommended_ids = list(recommendations.keys())
    
    y_true = [ratings_dict.get(recipe_id, 0) for recipe_id in recommended_ids]

    if not y_true or sum(y_true) == 0:
        return 0.0

    y_score = [recommendations[recipe_id] for recipe_id in recommended_ids]
    
    y_true = np.array(y_true).reshape(1, -1)
    y_score = np.array(y_score).reshape(1, -1)

    # Handle case where k is larger than the number of recommendations
    k_val = min(k, len(recommended_ids))
    if k_val == 0:
        return 0.0

    return ndcg_score(y_true, y_score, k=k_val)

# --- START FIX 3: UPDATING `evaluate_recommendations_with_tp_fp_fn` ---
# This function now needs to accept the faiss index and related data
# to pass them down to 'Recommendation_healthy_recipes'.
def evaluate_recommendations_with_tp_fp_fn(df, faiss_index, normalized_embeddings_l2, unique_user_ids, similarity_threshold, test_size=0.3, top_k_values=[]):
    results = {}
    top_n_popular = 10 
    
    # 1. Generate recommendations using the NEW, efficient function
    recommendations, actual_ratings = Recommendation_healthy_recipes(
        df, faiss_index, normalized_embeddings_l2, unique_user_ids, similarity_threshold, top_n_popular
    )
    # --- (End of modification in this function) ---

    if not recommendations:
        logging.error("No recommendations were generated. Stopping evaluation.")
        return {}

    train_users, test_users = train_test_split(list(recommendations.keys()), test_size=test_size, random_state=42)
    
    if not test_users:
        logging.error("No test users available for evaluation.")
        return {}

    users_with_true_positives = []
    users_with_false_positives = []
    users_with_false_negatives = []

    for k in top_k_values:
        tp_dict = {}
        fp_dict = {}
        fn_dict = {}

        for user in test_users:
            user_actual_ratings = set(actual_ratings.get(user, {}).keys())
            user_recs_all = recommendations.get(user, {})
            sorted_recs = sorted(user_recs_all.items(), key=lambda item: item[1], reverse=True)
            recommended_recipe_ids_k = set([recipe_id for recipe_id, pop in sorted_recs[:k]])

            true_positives = len(recommended_recipe_ids_k.intersection(user_actual_ratings))
            if true_positives >= 1:
                users_with_true_positives.append(user)

            false_positives_count = len(recommended_recipe_ids_k - user_actual_ratings)
            if false_positives_count > 0:
                users_with_false_positives.append(user)

            false_negatives_count = len(user_actual_ratings - recommended_recipe_ids_k)
            if false_negatives_count > 0:
                users_with_false_negatives.append(user)

            tp_dict[user] = true_positives
            fp_dict[user] = false_positives_count
            fn_dict[user] = false_negatives_count

        precision_scores = []
        recall_scores = []
        f1_scores = []
        ndcg_scores = []

        for i, user in enumerate(test_users):
            tp = tp_dict[user]
            fp = fp_dict[user]
            fn = fn_dict[user]

            precision = tp / k if k > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0

            if precision + recall > 0:
                f1 = 2 * (precision * recall) / (precision + recall)
            else:
                f1 = 0

            sorted_recs_tuples = sorted(recommendations.get(user, {}).items(), key=lambda item: item[1], reverse=True)[:k]
            recs_for_ndcg = {recipe_id: pop for recipe_id, pop in sorted_recs_tuples}
            
            ndcg = calculate_ndcg(df, user, recs_for_ndcg, k)

            precision_scores.append(precision)
            recall_scores.append(recall)
            f1_scores.append(f1)
            ndcg_scores.append(ndcg)

        average_precision = sum(precision_scores) / len(precision_scores) if precision_scores else 0
        average_recall = sum(recall_scores) / len(recall_scores) if recall_scores else 0
        average_f1 = sum(f1_scores) / len(f1_scores) if f1_scores else 0
        average_ndcg = sum(ndcg_scores) / len(ndcg_scores) if ndcg_scores else 0

        results[k] = {
            'Precision': average_precision,
            'Recall': average_recall,
            'F1-score': average_f1,
            'NDCG': average_ndcg
        }

    count_users_with_true_positives = len(users_with_true_positives)
    count_users_with_false_negatives = len(users_with_false_negatives)
    Users_test=len(test_users)
    
    print(f"Number of Users in Test Set: {Users_test}")
    print(f"Number of Users with True Positives >= 1: {count_users_with_true_positives}")
    print(f"Number of Users with Fales Negatives >= 1: {count_users_with_false_negatives}")

    return results
# --- END FIX 3 ---


# --- START FIX 4: REPLACING `extract_recommendations_and_ratings` ---
# This function had the same memory crash problem.
# It is now replaced with the same efficient faiss index search.
def extract_recommendations_and_ratings(df, faiss_index, normalized_embeddings_l2, unique_user_ids, similarity_threshold, AUC_popular):
    recommendations = {}
    actual_ratings = {}

    logging.info("Running Faiss range search for AUC...")
    # 1. Search the index for ALL users at once.
    lims, D, I = faiss_index.range_search(normalized_embeddings_l2, similarity_threshold)
    logging.info("Faiss search complete.")

    num_users = len(unique_user_ids)
    for i in range(num_users):
        user_id = unique_user_ids[i]

        # 2. Get the results for user 'i'
        start_idx = lims[i]
        end_idx = lims[i+1]
        neighbor_indices = I[start_idx:end_idx]

        actual_ratings[user_id] = set(df[df['user_id'] == user_id]['recipe_id'])
        
        # 3. Filter out the user itself
        similar_users_indices = [idx for idx in neighbor_indices if idx != i]
        
        # 4. Collect recipes (same logic as before)
        similar_user_rated_recipes = set()
        for similar_user_index in similar_users_indices:
            similar_user_id = unique_user_ids[similar_user_index]
            similar_user_rated_recipes.update(df[df['user_id'] == similar_user_id]['recipe_id'])

        # 5. Calculate popularity and get top N (same logic as before)
        recipe_popularity = {}
        for recipe_id in similar_user_rated_recipes:
            recipe_popularity[recipe_id] = len(df[df['recipe_id'] == recipe_id])

        popular_recipes = sorted(recipe_popularity.items(), key=lambda x: x[1], reverse=True)[:AUC_popular]
        recommended_recipes = [recipe_id for recipe_id, _ in popular_recipes]

        recommendations[user_id] = recommended_recipes

    return recommendations, actual_ratings
# --- END FIX 4 ---

def calculate_Recommendation_AUC(predictions, actual_ratings, test_size=0.2):
    true_labels = []
    predicted_scores = []

    for user_id, recommended_recipes in predictions.items():
        rated_recipes = actual_ratings.get(user_id, set())

        if recommended_recipes:
            try:
                train_set, test_set = train_test_split(recommended_recipes, test_size=test_size, random_state=42)
            except ValueError:
                test_set = recommended_recipes

            for i, recipe_id in enumerate(test_set):
                if recipe_id in rated_recipes:
                    true_labels.append(1)
                else:
                    true_labels.append(0)
                predicted_scores.append(len(recommended_recipes) - i)

    if len(true_labels) == 0 or len(set(true_labels)) <= 1:
        logging.warning("AUC calculation skipped: Not enough data or only one class present.")
        return 0.0
        
    auc = roc_auc_score(true_labels, predicted_scores)

    return auc

#----------------------------------------------------
def main():

    process_data(df)
    Heterogeneous_Graph(df)
    paths_tensor, meta_path = find_paths_users_interests(df)
    
    num_users = len(df['user_id'].unique())
    num_recipes = len(df['recipe_id'].unique())
    num_ingredients = len(df['ingredients'].unique())
    num_nutrition = len(df['nutrition'].unique())
    
    if num_users == 0 or num_recipes == 0 or num_ingredients == 0 or num_nutrition == 0:
        logging.error("Empty data. Cannot proceed with model training.")
        return

    user_encoder = LabelEncoder()
    recipe_encoder = LabelEncoder()
    ingredient_encoder = LabelEncoder()
    nutrition_encoder= LabelEncoder()
    user_encoder.fit(df['user_id'])
    recipe_encoder.fit(df['recipe_id'])
    ingredient_encoder.fit(df['ingredients'])
    nutrition_encoder.fit(df['nutrition'])
    
    # --- START FIX 5: Get sorted list of unique users ---
    # We need this to map faiss indices back to user IDs
    unique_user_ids = np.sort(df['user_id'].unique())
    # --- END FIX 5 ---
    
    embedding_dim = 64
    nla_model = NLA(num_users, num_recipes, num_ingredients, num_nutrition, embedding_dim, paths_tensor)
    NLA_loss = nla_model.train_nla(df, user_encoder, recipe_encoder, ingredient_encoder, nutrition_encoder, num_epochs=50)
    
    uid_tensor = torch.LongTensor(list(range(num_users)))
    rid_tensor = torch.LongTensor(list(range(num_recipes)))
    ing_tensor = torch.LongTensor(list(range(num_ingredients)))
    nut_tensor = torch.LongTensor(list(range(num_nutrition)))
    
    # Get the user embeddings directly from the layer's weight
    with torch.no_grad():
        embeddings_nla = nla_model.user_embedding.weight.clone()

    logging.info("Embedding Vectors (NLA):")
    logging.info(embeddings_nla)
    
    sla_for_healthy_foods = SLA(num_users, num_recipes, num_ingredients, num_nutrition, embedding_dim, paths_tensor, is_healthy=True)
    sla_for_healthy_foods.train_sla(uid_tensor, rid_tensor, ing_tensor, nut_tensor, num_epochs_sla=50)

    # Get the user embeddings from the SLA model
    with torch.no_grad():
        embeddings_for_healthy_foods = sla_for_healthy_foods.user_embedding.weight.clone()

    min_size = min(embeddings_nla.shape[0], embeddings_for_healthy_foods.shape[0])
    embeddings_nla = embeddings_nla[:min_size]
    embeddings_for_healthy_foods = embeddings_for_healthy_foods[:min_size]

    max_embedding_dim = max(embeddings_nla.shape[1], embeddings_for_healthy_foods.shape[1])

    padding_dim_nla = max_embedding_dim - embeddings_nla.shape[1]
    padding_dim_healthy = max_embedding_dim - embeddings_for_healthy_foods.shape[1]

    zero_padding_nla = torch.zeros(embeddings_nla.shape[0], padding_dim_nla)
    zero_padding_healthy = torch.zeros(embeddings_for_healthy_foods.shape[0], padding_dim_healthy)

    embeddings_nla = torch.cat((embeddings_nla, zero_padding_nla), dim=1)
    embeddings_for_healthy_foods = torch.cat((embeddings_for_healthy_foods, zero_padding_healthy), dim=1)

    summed_embeddings = embeddings_nla + embeddings_for_healthy_foods

    # Normalize the SUMMED embeddings
    normalized_embeddings = normalize_summed_embeddings(summed_embeddings)

    ground_truth_ratings = load_ground_truth_ratings(files_to_read, folder_path)
       
    #*****************************
    
    # --- START FIX 6: BUILD FAISS INDEX ---
    # This is the core of the fix. We build an index ONCE,
    # which can then be queried instantly without high RAM.
    
    # 1. L2 normalize embeddings for cosine similarity (Inner Product) in Faiss
    # 'normalized_embeddings' are MinMax scaled, not L2 normalized
    logging.info("L2 normalizing embeddings for Faiss...")
    normalized_embeddings_l2 = normalize(normalized_embeddings, norm='l2', axis=1).astype('float32')

    # 2. Create and train the Faiss index
    logging.info("Building Faiss index...")
    d = normalized_embeddings_l2.shape[1]  # Get embedding dimension
    index = faiss.IndexFlatIP(d)           # Using Inner Product (IP) for cosine similarity
    index.add(normalized_embeddings_l2)    # Add all user embeddings to the index
    logging.info(f"Faiss index built with {index.ntotal} vectors.")
    # --- END FIX 6 ---

    similarity_threshold = 0.9
    top_k_values = [10]
    top_n_popular = 10
    test_size=0.3
    
    # Call the evaluation function with the new arguments
    results = evaluate_recommendations_with_tp_fp_fn(
        df, index, normalized_embeddings_l2, unique_user_ids, similarity_threshold, test_size, top_k_values=top_k_values
    )
        
    k_values = list(results.keys())
    print("Results for Different Values of k:")
    print("=" * 60)
    print(f"{'k':<5}{'Precision':<15}{'Recall':<15}{'F1-score':<15}{'NDCG':<15}")
    print("=" * 60)

    for k in k_values:
        metrics = results[k]
        precision = metrics['Precision']
        recall = metrics['Recall']
        f1_score = metrics['F1-score']
        ndcg = metrics['NDCG']
        print(f"{k:<5}{' ':<5}{precision:.4f}{' ':<5}{recall:.4f}{' ':<5}{f1_score:.4f}{' ':<5}{ndcg:.4f}")     
        
    # Calculate AUC_Recipe
    AUC_popular=20
    # Call the other fixed function with the new arguments
    recommendations, actual_ratings = extract_recommendations_and_ratings(
        df, index, normalized_embeddings_l2, unique_user_ids, similarity_threshold, AUC_popular
    )
    auc_score = calculate_Recommendation_AUC(recommendations, actual_ratings, test_size)

    print(f"AUC Score: {auc_score}")
  
if __name__ == "__main__":
    main()
