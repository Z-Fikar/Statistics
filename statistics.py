import time as t
now = t.time()
import plotly
import plotly.graph_objs as go

from math import ceil, sqrt, log10, floor

li = [170.2, 171.3, 176.3, 177.0, 172.0, 165.6, 176.6, 169.5, 160.3, 170.0,
      174.3, 169.2, 168.3, 169.5, 177.6, 178.3, 170.4, 178.8, 170.3, 175.8,
      177.1, 178.4, 174.1, 170.0, 177.4, 169.8, 175.7, 168.5, 175.3, 179.8,
      162.3, 161.5, 170.6, 165.4, 175.0, 175.0, 173.2, 172.8, 168.6, 174.2,
      175.0, 178.0, 166.0, 166.0, 172.5, 167.5, 166.4, 170.7, 181.0, 175.5,
      165.0, 163.8, 179.7, 167.0, 169.0, 164.3, 162.0, 176.0, 170.5, 172.0,
      175.0, 173.0, 176.5, 166.6, 178.1, 170.0, 171.0, 172.0, 166.0, 179.3,
      176.5, 171.0, 169.3, 166.4, 170.3, 174.1, 175.0, 175.4, 176.4, 171.8,
      173.4, 169.0, 162.1
      ]
manual = 0
oli = li
bulat = 'atas'

def masuk(path=''):
    global li, oli, manual
    manual = 0
    if path == '':
        n = eval(input('Masukkan jumlah data: '))
        li = []
        for i in range(n):
            li.append(eval(input('# %2d | ' % (i+1))))
    else:
        try:
            with open(path, 'r') as f:
                li = [float(x) for x in f.read().split('\n')]
        except FileNotFoundError:
            print("File '%s' tidak dapat ditemukan." % path)
            reset()


def reset():
    global li, oli, manual, bulat
    li = oli
    manual = 0
    bulat = 'atas'


def cetak():
    i = 0
    print('Data:')
    for x in li:
        i += 1
        print('%5.2f' % x, end=" ")
        if i % 10 == 0:
            print()
    print()

def jkelas(bulat = ''):
    jumlah = 1 + 3.3*log10(len(li))
    if bulat == 'atas':
        return ceil(jumlah)
    elif bulat == 'bawah':
        return floor(jumlah)
    else:
        bulat = input('%f \nPembulatan ke atas atau ke bawah? [atas/bawah] ' % jumlah)
        jkelas(bulat)



def lkelas():
    return ceil((max(li)-min(li)) / jkelas(bulat))


def frekuensi(bb, ba):
    f = 0
    for x in li:
        if x >= bb and x <= ba:
            f += 1
    return f


def tabel():
    global manual, bulat
    koma = 0
    fk1 = 0
    fk2 = len(li)
    frk1 = 0
    frk2 = 100
    head = '| %2s | %13s | %12s | %9s | %11s | %13s | %17s |'\
        % ('No', 'Kelas    ', 'Titik Tengah', 'Frekuensi', 'F. Relatif', 'F. Kumulatif', 'F. RK      ')
    line = '+'+'-'*(len(head)-2)+'+'
    print (line + '\n' + head + '\n' + line)
    for kelas in range(int(jkelas(bulat))):
        bb = int(min(li)) + lkelas()*kelas
        ba = bb + lkelas()-1 + manual
        f = frekuensi(bb, ba)
        fr = f / len(li) * 100
        print('| %2d | %5.1f - %5.1f | %12.2f | %9d | %9.1f %% | %5d | %5d | %5.1f %% | %5.1f %% |'
              % (kelas+1, bb, ba, titikTengah(bb, ba), f, fr, fk1, fk2, frk1, frk2))
        fk1 += f
        fk2 -= f
        frk1 += fr
        frk2 -= fr
    print(line)
    print('| %2s   %5s   %5s   %12s | %9d | %9.1f %% | %5d | %5d | %5.1f %% | %5.1f %% |'
          % (' ', ' ', ' ', ' ', fk1, frk1, fk1, fk2, frk1, frk2))
    print(line)
    print('Menampilkan [%d / %d] data.' % (fk1, len(li)))
    if fk1 != len(li):
        print('Koreksi batas atas..')
        for x in li:
            if koma < x%1:
                koma = x%1
        manual = koma
        if manual == 0:
            print('Koreksi jumlah kelas..')
            bulat = 'bawah'
        tabel()


def mean():
    ttf = []
    for kelas in range(int(jkelas(bulat))):
        bb = int(min(li)) + lkelas()*kelas
        ba = bb + lkelas()-1 + manual
        f = frekuensi(bb, ba)
        ttf.append(titikTengah(bb, ba)*f)
    return sum(x for x in ttf) / len(li)


def titikTengah(bb, ba):
    return (ba+bb) / 2


def median():
    fk = 0
    mid = len(li) / 2
    for kelas in range(int(jkelas(bulat))):
        bb = int(min(li)) + lkelas()*kelas
        ba = bb + lkelas()-1 + manual
        f = frekuensi(bb, ba)
        if fk+f > mid:
            return (bb - 0.5 + manual/2) + (mid-fk)*lkelas()/f
        fk += f


def modus():
    f = []
    tb = []
    for kelas in range(int(jkelas(bulat))):
        bb = int(min(li)) + lkelas()*kelas
        ba = bb + lkelas()-1 + manual
        f.append(frekuensi(bb, ba))
        tb.append(bb - 0.5 + manual/2)
    for i in range(len(f)):
        if max(f) == f[i]:
            return tb[i] + (f[i] - f[i-1])*lkelas() / ((f[i] - f[i-1]) + (f[i] - f[i+1]))


def gmean():
    result = 1
    for kelas in range(int(jkelas(bulat))):
        bb = int(min(li)) + lkelas()*kelas
        ba = bb + lkelas()-1 + manual
        result *= titikTengah(bb, ba) ** frekuensi(bb, ba)
    return result ** (1/len(li))


def quartil(n):
    if n > 0 and n < 4:
        q = len(li) * n / 4
        fk = 0
        for kelas in range(int(jkelas(bulat))):
            bb = int(min(li)) + lkelas()*kelas
            ba = bb + lkelas()-1 + manual
            f = frekuensi(bb, ba)
            if (fk+f) > q:
                return (bb - 0.5 + manual/2) + (q-fk)*lkelas()/f
            fk += f
    else:
        return 'Error: quartil(n) , n = 1 ~ 3'


def quantil(n):
    if n > 0 and n < 5:
        q = len(li) * n / 5
        fk = 0
        for kelas in range(int(jkelas(bulat))):
            bb = int(min(li)) + lkelas()*kelas
            ba = bb + lkelas()-1 + manual
            f = frekuensi(bb, ba)
            if (fk+f) > q:
                return (bb - 0.5 + manual/2) + (q-fk)*lkelas()/f
            fk += f
    else:
        return 'Error: quantil(n) , n = 1 ~ 4'


def tetril(n):
    if n > 0 and n < 10:
        t = len(li) * n / 10
        fk = 0
        for kelas in range(int(jkelas(bulat))):
            bb = int(min(li)) + lkelas()*kelas
            ba = bb + lkelas()-1 + manual
            f = frekuensi(bb, ba)
            if (fk+f) > t:
                return (bb - 0.5 + manual/2) + (t-fk)*lkelas()/f
            fk += f
    else:
        return 'Error: tetril(n) , n = 1 ~ 9'


def persentil(n):
    if n > 0 and n < 100:
        p = len(li) * n / 100
        fk = 0
        for kelas in range(int(jkelas(bulat))+1):
            bb = int(min(li)) + lkelas()*kelas
            ba = bb + lkelas()-1 + manual
            f = frekuensi(bb, ba)
            if (fk+f) > p:
                return (bb - 0.5 + manual/2) + (p-fk)*lkelas()/f
            fk += f
    else:
        return 'Error: persentil(n) , n = 1 ~ 99'


def rangeq():
    return (quartil(3)-quartil(1))/2


def SR():
    result=0
    for kelas in range(int(jkelas(bulat))):
        bb = int(min(li)) + lkelas()*kelas
        ba = bb + lkelas()-1 + manual
        f = frekuensi(bb, ba)
        result += abs(titikTengah(bb, ba)-mean()) * f
    return result / len(li)


def ragam():
    result = 0
    for kelas in range(int(jkelas(bulat))):
        bb = int(min(li)) + lkelas()*kelas
        ba = bb + lkelas()-1 + manual
        f = frekuensi(bb, ba)
        result += (titikTengah(bb, ba)-mean()) ** 2 * f
    return result/len(li)


def SB():
    return sqrt(ragam())


def menu_df():
    print ('Distribusi Frekuensi')
    print('Jumlah Data  : %5d' % len(li))
    print('Maximum      : %5.1f' % max(li))
    print('Minimum      : %5.1f' % min(li))
    print('Jangkauan    : %5.1f' % (max(li)-min(li)))
    print('Jumlah Kelas : %5d' % jkelas(bulat))
    print('Lebar Kelas  : %5d' % lkelas())


def menu_upt():
    print('Ukuran Pusat')
    print('Mean          : %6.2f' % mean())
    print('Median        : %6.2f' % median())
    print('Modus         : %6.2f' % modus())
    print('Rata-rata ukur: %6.3f' % gmean())


def menu_upb():
    print('Ukuran Penyebaran')
    print('Range               : %6.3f' % (max(li)-min(li)))
    print('Range Quartil       : %6.3f' % (rangeq()))
    print('Simpangan Rata-rata : %6.3f' % (SR()))
    print('Ragam               : %6.3f' % (ragam()))
    print('Simpangan Baku      : %6.3f' % (SB()))


def diagram(mode = ''):
    datax = []
    datay = []
    judul = ''
    for kelas in range(int(jkelas(bulat))):
        bb = int(min(li)) + lkelas()*kelas
        ba = bb + lkelas()-1 + manual
        datax.append(titikTengah(bb, ba))
        datay.append(frekuensi(bb, ba))
    if li == oli:
        datax = ['%.2f cm' % z for z in datax]
        judul = 'Average Male Height'
    dicts = {"data": [go.Scatter(x=datax,
                                 y=datay
                                 ),
                      go.Bar(x=datax,
                             y=datay
                             )
                      ],
             "layout": go.Layout(title=judul,
                                 xaxis=dict(title='Titik Tengah'),
                                 yaxis=dict(title='Frekuensi')
                                 )
             }
    if mode == 'notebook':
        plotly.offline.init_notebook_mode()
        plotly.offline.iplot(dicts)
    else:
        print('Membuka dengan peramban bawaan.')
        plotly.offline.plot(dicts)


def main():
    global mode
    print('\nMenu Statistika:')
    print(' 0. Exit')
    print(' 1. Cetak Data')
    print(' 2. Ganti Data')
    print(' 3. Distribusi Frekuensi')
    print(' 4. Ukuran Pusat')
    print(' 5. Ukuran Penyebaran')
    print(' 6. Quartil')
    print(' 7. Quantil')
    print(' 8. Tetril')
    print(' 9. Persentil')
    print('10. Diagram')
    opsi = eval(input('>>> '))
    if opsi == 0:
        exit()
    elif opsi == 1:
        cetak()
    elif opsi == 2:
        ganti = ''
        while ganti != 'file' and ganti != 'manual' and ganti != 'reset':
            ganti = input('Dengan [file/manual/reset]: ')
        if ganti == 'file':
            masuk(input('Masukkan alamat dan/atau nama File: '))
        elif ganti == 'manual':
            masuk()
        elif ganti == 'reset':
            reset()
        else:
            print('Input salah!')
        cetak()
    elif opsi == 3:
        menu_df()
        tabel()
    elif opsi == 4:
        menu_upt()
    elif opsi == 5:
        menu_upb()
    elif opsi == 6:
        print('=', quartil(eval(input('Quartil ke - '))))
    elif opsi == 7:
        print('=', quantil(eval(input('Quantil ke - '))))
    elif opsi == 8:
        print('=', tetril(eval(input('Tetril ke - '))))
    elif opsi == 9:
        print(persentil(eval(input('Persentil ke - '))))
    elif opsi == 10:
        diagram(mode)
    main()


print('Waktu inisialisasi: %.2f detik' % (t.time()-now))
