function dehaze(input_image, output_image)
    system(['curl -F "file=@' input_image '" http://172.20.53.144:1718/dehaze'])
    remain = input_image;
    name_str = {};
    while true
        [str, remain] = strtok(remain, '\');
        if isempty(str),  break;  end
        name_str = [name_str str];
    end
    input_image = name_str{length(name_str)};
    remain = input_image;
    name_str = {};
    while true
        [str, remain] = strtok(remain, '.');
        if isempty(str),  break;  end
        name_str = [name_str str];
    end
    name_str{length(name_str) - 1} = [name_str{length(name_str) - 1} '_rerad'];
    dehaze_image = name_str{1};
    for i = 1 : length(name_str) - 1
        dehaze_image = [dehaze_image '.' name_str{i+1}];
    end
    dehaze_image = ['http://172.20.53.144:1718/static/result/' dehaze_image];
    urlwrite(dehaze_image, output_image);
end