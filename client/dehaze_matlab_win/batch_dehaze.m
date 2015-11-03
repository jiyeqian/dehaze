input_dir = '~/';
output_dir = '~/aa/';
files = dir(fullfile(input_dir, '*.jpg'));
% files = files.name
for i = 1 : length(files)
    input_image = fullfile(input_dir,  files(i).name);
    output_image = fullfile(output_dir, [files(i).name, '_dehaze.jpg']);
    dehaze(input_image, output_image);
end