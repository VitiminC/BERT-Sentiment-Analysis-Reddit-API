from src.config.config import *
from src.utils.sql_loader import DataSqlLoader


def ocr_detector(submission_imgpath, output_dir='result/'):
    refine_net = load_refinenet_model(cuda=True)
    craft_net = load_craftnet_model(cuda=True)

    for image_path in sorted(os.listdir(submission_imgpath)):
        image_path = os.path.join(submission_imgpath, image_path)
        image = read_image(image_path)

        prediction_result = get_prediction(
            image=image,
            craft_net=craft_net,
            refine_net=refine_net,
            text_threshold=0.7,
            link_threshold=0.4,
            low_text=0.4,
            cuda=True,
            long_size=1280
        )

        if len(prediction_result['boxes']) > 0:
            exported_file_paths = export_detected_regions(
                image_path=image_path,
                image=image,
                regions=prediction_result["boxes"],
                output_dir=output_dir,
                rectify=True
            )
            print(exported_file_paths)
            export_extra_results(
                image_path=image_path,
                image=image,
                regions=prediction_result["boxes"],
                heatmaps=prediction_result["heatmaps"],
                output_dir=output_dir
            )
        empty_cuda_cache()
