# 1.Aşama: Veri Hazırlama
# --------------------------------------------------------------------------------------

# movie: movieId, film adı ve filmin tür bilgilerini içeren veri seti
# rating: UserID, film adı, filme verilen oy ve zaman bilgisini içeren veri seti
# Ratingdeki kullanıcıların oy kullandıkları filmlerin sadece id'si var.
# Idlere ait film isimlerini ve türünü movie veri setinden ekliyoruz. ve df dataframe i oluşturuyoruz.
# Herbir film için toplam kaç kişinin oy kullanıldığını hesaplıyoruz. (comment_counts)
# Oy kullanma sayısı 1000'in altında olan filmleri rare_movies de tutuyoruz.
# common_movies de yaygın filmleri tutuyoruz.
# common_movies dataframe için pivot table oluşturuyoruz.
import pandas as pd

def create_user_movie_df():
    movie = pd.read_csv('datasets/movie.csv')
    rating = pd.read_csv('datasets/rating.csv')
    df = movie.merge(rating, how="left", on="movieId")
    comment_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comment_counts[comment_counts["title"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df

user_movie_df = create_user_movie_df()
user_movie_df.head()

# 2.Aşama: Elimizdeki kullanıcının izlediği filmleri bulmalıyız.
# --------------------------------------------------------------------------------------

random_user = 108170

# Belirlemiş olduğumuz usera göre veriyi indirgeme
random_user_df = user_movie_df[user_movie_df.index == random_user]

# Kullanıcının oy kullandığı filmleri ele alıyoruz.
movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()

# Oylanan film sayısı
len(movies_watched)

# 3.Aşama: Aynı filmleri izleyen kullanıcıların id'lerini buluyoruz.
# --------------------------------------------------------------------------------------

# Seçtiğimiz kullanıcının izlediği fimlere ait sutunları user_movie_df'ten seçiyoruz ve yeni df oluşturuyoruz.
movies_watched_df = user_movie_df[movies_watched]

# Herbir kullancının seçili user'in izlediği filmlerin kaçını izlediğini hesaplıyoruz
user_movie_count = movies_watched_df.T.notnull().sum()
user_movie_count = user_movie_count.reset_index()
user_movie_count.columns = ["userId", "movie_count"]
user_movie_count.sort_values("movie_count", ascending=True)

# Bizim kullanıcımız ile benzer filmlerin en az %60 ını izleyenleri alıyoruz.
perc = len(movies_watched) * 60 / 100
users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]

# %60 üzeri benzer filmlere oy veren user sayısı
len(users_same_movies)

# 4.Aşama: Öneri Yapılacak Kullanıcı ile En Benzer Kullanıcıların Belirlenmesi
# --------------------------------------------------------------------------------------

# Bizim kullanıcı ve en çok benzeyen kullanıcıları ele aldık.
final_df = movies_watched_df[movies_watched_df.index.isin(users_same_movies)]

# Sutünlarda userlar olması gerekiyor. Bunun için final_df'in transpozu alınarak userlar sutüne alınmıştır.
corr_df = final_df.T.corr().unstack().sort_values()
corr_df = pd.DataFrame(corr_df, columns=["corr"])
corr_df.index.names = ['user_id_1', 'user_id_2']
corr_df = corr_df.reset_index()

# Belirlemiş olduğumuz user, diğer kolonda tüm userlar ve bunlar arasındaki korelasyonu 0.65'den büyük ve eşit olanlar
# Belirlemiş olduğumuz user ile %65 korelasyona sahip olanlar getirilmesi ve yeni bir dataframe basılması.
top_users = corr_df[(corr_df["user_id_1"] == random_user) & (corr_df["corr"] >= 0.65)][["user_id_2", "corr"]].reset_index(drop=True)

# Bizim kullanıcımız ile korelasyonu en yüksek kullanıcıları bulduk.
top_users = top_users.sort_values(by='corr', ascending=False)
top_users.rename(columns={"user_id_2": "userId"}, inplace=True)

# Bu kullanıcıların id bilgileri ile hangi filme kaç puan verdiklerine bakıyoruz.
rating = pd.read_csv('datasets/rating.csv')

# Bu tabloda çoklamalar var neden? Bir kullanıcı birden çok filme puan vermiş olabilir.
top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')

# Kendi kullanıcımızı bulduğumuz kullanıcılar arasından çıkarıyoruz.
top_users_ratings = top_users_ratings[top_users_ratings["userId"] != random_user]

# Adım 5: Weighted Average Recommendation Score'un Hesaplanması ve User-Based ile 5 Film Önerisi
# ----------------------------------------------------------------------------------------------

# Korelasyon ve rating değerlerini öneri için kullanıyoruz. Kullanıcılar aynı filmleri izlemiş olabilir,
# bu durumda filmler çoklar.
# Bunu engellemek için filmlere göre grupluyoruz ve weighted_ratingin mean değerini alıyoruz.
top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']
top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})

recommendation_df = top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})
recommendation_df = recommendation_df.reset_index()

# weighted_rating'i 3.5'ten büyük olanları getirelim: Önerilecek filmler
recommendation_df[recommendation_df["weighted_rating"] > 3.5]
movies_to_be_recommend = recommendation_df[recommendation_df["weighted_rating"] > 3.5].sort_values("weighted_rating",
                                                                                                 ascending=False)[0:5]
# movie verisetinden filmlerin isimlerine erişelim.
movie = pd.read_csv('datasets/movie.csv')
movies_to_be_recommend.merge(movie[["movieId", "title"]]).index

movies_to_be_recommend.merge(movie[["movieId", "title"]])["title"]