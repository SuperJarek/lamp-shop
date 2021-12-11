<html>
 <head>
  <title>PHP Test</title>
 </head>
 <body>
 
 <?php 
//var_dump ($json_data);
if (!defined('_PS_ADMIN_DIR_')) {
    define('_PS_ADMIN_DIR_', getcwd());
}
include(_PS_ADMIN_DIR_.'/../config/config.inc.php');

//authorisation();

$categories_cache = [];
$products_loaded_indicator_file = './lamps/products_loaded_indicator';
if (!file_exists($products_loaded_indicator_file))
{
    addProducts();
     
    fclose(fopen($products_loaded_indicator_file,"w"));
    echo '<p>Hello World</p>'; 
}
echo '<p>Done</p>'; 

function addProducts()
{
    $json = file_get_contents('./lamps/items_data.json');
    $json_products = json_decode($json,true);

    foreach ($json_products as &$json_product) {
        addProduct(
            $json_product["attributes"]["Kod EAN:"],
            $json_product["name"],
            $json_product["description"],
            $json_product["price_pln"],
            $json_product["main_photo_uri"],
            $json_product["photos"],
            $json_product["categories"],
            $json_product["attributes"]
        );
    }
}
 
function addProduct($ean13, $name, $desc, $price, $main_photo_uri, $photos, $categories, $attributes) 
{
   $product = new Product();   
   $product->ean13 = $ean13;
   $product->reference = $name;
   $product->name = createMultiLangField($name);
   $product->meta_description = $name;
   $product->description = htmlspecialchars($desc);
   $product->price = number_format($price/1.23, 6, '.', '');
   $product->link_rewrite = createMultiLangField(Tools::str2url($name));
   $product->redirect_type = '301';
   
   $product->show_price = 1;
   $product->minimal_quantity = 1;
   
   $cat_ids = addCategoriesToProduct($product, $categories);
   $product->add();
   StockAvailable::setQuantity($product->id, null, 10);
   $product->addToCategories($cat_ids); // ([3])
   
   addAttributesToProduct($product, $attributes);
   
   if (empty($photos))
       addPhotoToProduct($product, $main_photo_uri, 0);
   else
        addPhotosToProduct($product, $photos);
   //addPhotoToProduct($product, $main_photo_uri);
   
   
   echo "<br>";echo "<br>";
   echo "Success! <br>";
}

function addPhotosToProduct($product, $photos)
{
    var_dump ($photos);
    foreach ($photos as $index => $photo){
        var_dump ($index);
        var_dump ($photo); echo '<br/>';
        addPhotoToProduct($product, $photo, $index);
    }
}

function addCategoriesToProduct($product, $categories)
{
    global $categories_cache;
    $cat_ids = [2];
    foreach ($categories as &$category_name) {
        if (array_key_exists($category_name, $categories_cache)){
            array_push($cat_ids, $categories_cache[$category_name]);
        }
        else {
            $new_cat_id = addCategory($category_name, end($cat_ids));
            $categories_cache[$category_name] = $new_cat_id;
            array_push($cat_ids, $new_cat_id);
        }
    }
   $product->id_category_default = end($cat_ids);
   return $cat_ids;
}

function addCategory($category_name, $parent_category)
{
    $category = new Category();
    $category->name = createMultiLangField($category_name);
    $category->id_parent = $parent_category;
    $category->link_rewrite = createMultiLangField(Tools::str2url($category_name));
    $category->description = $category_name;
    $category->active = 1;
    
    $category->meta_title = $category_name;
    $category->meta_description = $category_name;
    $category->meta_keywords = array($category_name);
    
    if (!Validate::isLoadedObject($category))
        echo "ERROR<br>";
    $category->add();
    
    return $category->id;
}

function addPhotoToProduct($product, $imgUri, $position)
{
    $shops = Shop::getShops(true, null, true);
    $image = new Image();
    $image->id_product = $product->id;
    $image->position = $position; //Image::getHighestPosition($product->id) + 1;
    if ($position == 0)
        $image->cover = true;
    if (($image->validateFields(false, true)) === true && ($image->validateFieldsLang(false, true)) === true && $image->add()) 
    {
        $image->associateTo($shops);
        if (!uploadImage($product->id, $image->id, $imgUri)) {
            echo "<br><br> Failed to add image! <br>";
            $image->delete();
        }
        else {
            echo "<br><br> Image add successful!<br>";
        }
    }
}

function uploadImage($id_entity, $id_image = null, $imgUri) {
    $tmpfile = tempnam(_PS_TMP_IMG_DIR_, 'ps_import');
    $watermark_types = explode(',', Configuration::get('WATERMARK_TYPES'));
    $image_obj = new Image((int)$id_image);
    $path = $image_obj->getPathForCreation();
    $imgUri = str_replace(' ', '%20', trim($imgUri));
    // Evaluate the memory required to resize the image: if it's too big we can't resize it.
    if (!ImageManager::checkImageMemoryLimit($imgUri)) {
            echo "<br><br> Image add failed1!<br>";
        return false;
    }
    if (@copy($imgUri, $tmpfile)) {
        ImageManager::resize($tmpfile, $path . '.jpg');
        $images_types = ImageType::getImagesTypes('products');
        foreach ($images_types as $image_type) {
            ImageManager::resize($tmpfile, $path . '-' . stripslashes($image_type['name']) . '.jpg', $image_type['width'], $image_type['height']);
            if (in_array($image_type['id_image_type'], $watermark_types)) {
            Hook::exec('actionWatermark', array('id_image' => $id_image, 'id_product' => $id_entity));
            }
        }
    } else {
        unlink($tmpfile);
            echo "<br><br> Image add failed2!<br>";
        return false;
    }
    unlink($tmpfile);
            echo $imgUri; echo '<br>';
            echo $id_image; echo '<br>';
            echo "<br><br> Image add Successful1!<br>";
    return true;
}
 
function addAttributesToProduct($product, $attributes)
{
    foreach ($attributes as $attributeName => $attributeValue) {
               // 1. Check if 'feature name' exist already in database
               $FeatureNameId = Db::getInstance()->getValue('SELECT id_feature FROM ' . _DB_PREFIX_ . 'feature_lang WHERE name = "' . pSQL($attributeName) . '"');
               // If 'feature name' does not exist, insert new.
               if (empty($FeatureNameId)) {
                   Db::getInstance()->execute('INSERT INTO `' . _DB_PREFIX_ . 'feature` (`id_feature`,`position`) VALUES (0, 0)');
                   $FeatureNameId = Db::getInstance()->Insert_ID(); // Get id of "feature name" for insert in product
                   Db::getInstance()->execute('INSERT INTO `' . _DB_PREFIX_ . 'feature_shop` (`id_feature`,`id_shop`) VALUES (' . $FeatureNameId . ', 1)');
                   Db::getInstance()->execute('INSERT INTO `' . _DB_PREFIX_ . 'feature_lang` (`id_feature`,`id_lang`, `name`) VALUES (' . $FeatureNameId . ', ' . Context::getContext()->language->id . ', "' . pSQL($attributeName) . '")');
               }
               
               // 1. Check if 'feature value name' exist already in database
               $FeatureValueId = Db::getInstance()->getValue('SELECT id_feature_value FROM ' . _DB_PREFIX_ . 'feature_value WHERE id_feature_value IN (SELECT id_feature_value FROM `' . _DB_PREFIX_ . 'feature_value_lang` WHERE value = "' . pSQL($attributeValue) . '") AND id_feature = ' . $FeatureNameId);
               // If 'feature value name' does not exist, insert new.
               if (empty($FeatureValueId)) {
                   Db::getInstance()->execute('INSERT INTO `' . _DB_PREFIX_ . 'feature_value` (`id_feature_value`,`id_feature`,`custom`) VALUES (0, ' . $FeatureNameId . ', 0)');
                   $FeatureValueId = Db::getInstance()->Insert_ID();
                   Db::getInstance()->execute('INSERT INTO `' . _DB_PREFIX_ . 'feature_value_lang` (`id_feature_value`,`id_lang`,`value`) VALUES (' . $FeatureValueId . ', ' . Context::getContext()->language->id . ', "' . pSQL($attributeValue) . '")');
               }
               Db::getInstance()->execute('INSERT INTO `' . _DB_PREFIX_ . 'feature_product` (`id_feature`, `id_product`, `id_feature_value`) VALUES (' . $FeatureNameId . ', ' . $product->id . ', ' . $FeatureValueId . ')');
           }
}

function createMultiLangField($field) {
    $res = array();
    foreach (Language::getIDs(false) as $id_lang) {
        $res[$id_lang] = $field;
    }
    return $res;
}

function authorization()
{
    $key = '7b2f3e5b-65f9-4dd8-a584-1fb3626e0a9f';
    if(!Tools::getValue('key') || Tools::getValue('key') != $key) {
        sleep(3);
        die();
    }
}
 
 ?> 
 </body>
</html>