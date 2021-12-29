# Hibrit Öneri Sistemi 

![image](https://user-images.githubusercontent.com/26279874/147696501-87c7bec4-12b4-4db4-b161-f9c807fc3757.png)

## İş Problemi
Film sitemiz olduğunu düşünelim ve bir kullanıcının Id bilgisi elimizdedir. Bu kullanıcıya yeni film tavsiyesi vermek istiyoruz.
User-based yöntemi kullanarak kullanıcıya en uygun filmleri önermeliyiz.

## Veri Seti Hikayesi

Elimizde iki adet veri seti bulunmaktadır. Bu veriler MovieLens tarafından rastgele kullanıcılar seçilerek oluşturulmuştur.
Veri setleri; filmler ve bu filmlere yapılan derecelendirme puanlarını barındırmaktadır.

## Veri Seti Değişkenleri

1- movie.csv
* movieId: Eşsiz film numarası (UniqueId)
* title: Film adı

2- rating.csv
* userId: Eşsiz kullanıcı numarası (UniqueId)
* movieId: Eşsiz film numarası (UniqueId)
* rating: Kullanıcı tarafından filme verilen puan
* timestamp: Dğerlendirme tarihi



