clc;
clear;
close all;

A = [1 7 1 7 2; 1 7 1 6 4; 1 7 1 6 8];
img_rows = 104;
img_columns = 200;
columns = [1,2,3];
B = zeros(img_rows, img_columns);

for i = 1 : 104
    for j = 1 : 5 : 201
        pick_column = randi(length(columns));
        row = A(pick_column:pick_column, :);
        position = randi(length(row));
        row(position) = 5;
        if (j ~= 201)
            B(i, j:j+4) = row;
        end
    end
end

% Arxikopioisi eikonas
I = mat2gray(B);

figure('Name', 'Random Image:');
imshow(I);
grid on

I1 = im2double(I);
T = dctmtx(8); % dct matrix
%Performing DCT on blocks of 8 by 8
dct = @(block_struct) T * block_struct.data * T';
B = blockproc(I1,[8 8],dct);
B = ceil(B); 
% A Standard Quantization Matrix
q_mtx = [16 11 10 16 24 40 51 61; 
              12 12 14 19 26 58 60 55;
              14 13 16 24 40 57 69 56; 
              14 17 22 29 51 87 80 62;
              18 22 37 56 68 109 103 77;
              24 35 55 64 81 104 113 92;
              49 64 78 87 103 121 120 101;
              72 92 95 98 112 100 103 99];
   %PErforming Quantization by Dividing with q_mtx on blocks of 8 by 8
   c = @(block_struct) (block_struct.data) ./ q_mtx;        
   B2 = blockproc(B,[8 8],c);
  %    B2 = ceil(B2)
%Performing Inverse Quantization By Multiplying with q_mtx on Blocks of 8
%by 8
B3 = blockproc(B2,[8 8],@(block_struct) q_mtx .* block_struct.data);
%Performing Inverse DCT on Blocks of 8 by 8
invdct = @(block_struct) T' * block_struct.data * T;
% B3 = ceil(B3);
I2 = blockproc(B3,[8 8],invdct);
figure('Name', 'Compressed Image using DCT:'), imshow(I2)
