import { View, Text, TextInput, TouchableOpacity, ScrollView, Alert, Image } from "react-native";
import { useState, useEffect } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import * as ImagePicker from "expo-image-picker";
import Apis, { authApis, endpoints } from "../../utils/Apis";
import CreateFoodStyle from "../../styles/CreateFoodStyle";
import FoodDetailStyle from "../../styles/FoodDetailStyle";

const CreateFood = ({ navigation, route }) => {
    const { foodId, isEdit } = route.params || {};

    const [foodName, setFoodName] = useState("");
    const [price, setPrice] = useState("");
    const [cookTime, setCookTime] = useState("");
    const [description, setDescription] = useState("");
    const [image, setImage] = useState(null);

    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState(null);

    const [ingredients, setIngredients] = useState([]);
    const [selectedIngredients, setSelectedIngredients] = useState([]);
    const [newIngredient, setNewIngredient] = useState("");

    const [loading, setLoading] = useState(false);
    const [ingredientPage, setIngredientPage] = useState(1);
    const [categoryPage, setCategoryPage] = useState(1);

    const loadCategories = async () => {
        try {
            const res = await Apis.get(endpoints['categories'],{
                params: { page: categoryPage }
            });
            setCategories(res.data.results || []);
        } catch (err) {
            console.error(err);
        }
    };

    const loadIngredients = async () => {
        try {
            const res = await Apis.get(endpoints['ingredients'], {
                params: { page: ingredientPage }
            });
            setIngredients(res.data.results || []);

            if (res.data.next == null)
                setIngredientPage(0);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        loadCategories();
    });

    useEffect(() => {
        if (ingredientPage > 0)
            loadIngredients();
    }, [ingredientPage]);

    const getAuthApi = async () => {
        const token = await AsyncStorage.getItem("access_token");
        if (!token) {
            Alert.alert("Lỗi", "Bạn chưa đăng nhập");
            return null;
        }
        return authApis(token);
    };


    const toggleIngredient = (name) => {
        setSelectedIngredients(prevSelected => {
            if (prevSelected.includes(name)) {
                return prevSelected.filter(item => item !== name);
            }
            return [...prevSelected, name];
        });
    };

    const createIngredient = async () => {
        try {
            const api = await getAuthApi();
            const res = await api.post(endpoints['ingredients'], {
                name: newIngredient
            });

            setIngredients(prev => [...prev, res.data]);
            setNewIngredient("");
        } catch (err) {
            console.error(err);
            Alert.alert("Lỗi", "Không thể tạo nguyên liệu");
        }
    };

    const pickImage = async () => {
        const { granted } = await ImagePicker.requestMediaLibraryPermissionsAsync();
        if (!granted) {
            Alert.alert("Không có quyền truy cập thư viện ảnh");
            return;
        }
        if (granted) {
            const res = await ImagePicker.launchImageLibraryAsync();
            if (!res.canceled)
                setImage(res.assets[0]);
        } else
            Alert.alert("Permission denied!");
    };

    const submitFood = async () => {
        if (!foodName || !price || !cookTime || !selectedCategory) {
            Alert.alert("Lỗi", "Vui lòng nhập đầy đủ thông tin");
            return;
        }

        try {
            setLoading(true);
            const token = await AsyncStorage.getItem("access_token");
            if (!token) {
                Alert.alert("Lỗi", "Bạn chưa đăng nhập");
                return;
            }

            const api = authApis(token);
            const payload = {
                name: foodName,
                price: price,                
                cook_time: Number(cookTime), 
                category_uuid: selectedCategory,
                description: description,
                ingredients: selectedIngredients, 
            };

            if (isEdit) {
                await api.put(
                    `${endpoints["foods"]}${foodId}/`,
                    payload
                );

                Alert.alert("Thành công", "Đã cập nhật món ăn", [
                    { text: "OK", onPress: () => navigation.goBack() }
                ]);
            } else {
                await api.post(
                    endpoints["foods"],
                    payload
                );

                Alert.alert("Thành công", "Đã tạo món ăn", [
                    { text: "OK", onPress: () => navigation.goBack() }
                ]);
            }
        } catch (err) {
            console.log("CREATE FOOD ERROR:", err.response?.data || err.message);
            Alert.alert("Lỗi", "Không thể lưu món ăn");
        } finally {
            setLoading(false);
        }
    };



    const loadFoodDetail = async () => {
        try {
            const res = await Apis.get(`${endpoints['foods']}${foodId}/`);

            const food = res.data;

            setFoodName(food.name);
            setPrice(String(food.price));
            setCookTime(String(food.cook_time));
            setDescription(food.description || "");
            setSelectedCategory(food.category?.uuid || null);

            setSelectedIngredients(
                food.ingredients?.map(i => i.uuid) || []
            );

            if (food.image) {
                setImage({ uri: food.image });
            }
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        if (isEdit && foodId) {
            loadFoodDetail();
        }
    }, [foodId]);

    return (
        <ScrollView style={CreateFoodStyle.container}>
            <TouchableOpacity onPress={() => navigation.goBack()}>
                <Text style={FoodDetailStyle.goBack}>{"<"}</Text>
            </TouchableOpacity>
            <Text style={CreateFoodStyle.title}>Tạo món ăn</Text>

            <TextInput
                placeholder="Tên món ăn"
                value={foodName}
                onChangeText={setFoodName}
                style={CreateFoodStyle.input}
            />

            <TextInput
                placeholder="Giá (VNĐ)"
                value={price}
                keyboardType="numeric"
                onChangeText={setPrice}
                style={CreateFoodStyle.input}
            />

            <TextInput
                placeholder="Thời gian chuẩn bị (phút)"
                value={cookTime}
                keyboardType="numeric"
                onChangeText={setCookTime}
                style={CreateFoodStyle.input}
            />

            <TextInput
                placeholder="Mô tả món ăn"
                value={description}
                onChangeText={setDescription}
                multiline
                numberOfLines={4}
                style={[CreateFoodStyle.input, { height: 100 }]}
            />

            {image && (<Image source={{ uri: image.uri }} style={CreateFoodStyle.previewImage}/>)}
            <TouchableOpacity
                style={CreateFoodStyle.imagePicker}
                onPress={pickImage}>
                <Text style={CreateFoodStyle.imagePickerText}>📷 Chọn ảnh món ăn (tuỳ chọn)</Text>
            </TouchableOpacity>
            

            <Text style={CreateFoodStyle.label}>Danh mục</Text>
            <View style={{ 
                flexDirection: "row",
                justifyContent: "space-between",
                marginVertical: 10
            }}>
                <TouchableOpacity
                    onPress={() => categoryPage > 1 && setCategoryPage(p => p - 1)}
                >
                    <Text>{"<="} Trang trước</Text>
                </TouchableOpacity>

                <TouchableOpacity
                    onPress={() => setCategoryPage(p => p + 1)}
                >
                    <Text>Trang sau {"=>"}</Text>
                </TouchableOpacity>
            </View>
            {categories.map(c => (
                <TouchableOpacity
                    key={c.uuid}
                    style={CreateFoodStyle.listItem}
                    onPress={() => setSelectedCategory(c.uuid)}
                >
                    <Text style={CreateFoodStyle.listText}>{c.name}</Text>
                    <Text style={CreateFoodStyle.radio}>
                        {selectedCategory === c.uuid ? "●" : "○"}
                    </Text>
                </TouchableOpacity>
            ))}

            <Text style={CreateFoodStyle.label}>Nguyên liệu</Text>
            <View style={{ 
                flexDirection: "row",
                justifyContent: "space-between",
                marginVertical: 10
            }}>
                <TouchableOpacity
                    onPress={() => ingredientPage > 1 && setIngredientPage(p => p - 1)}
                >
                    <Text>{"<="} Trang trước</Text>
                </TouchableOpacity>

                <TouchableOpacity
                    onPress={() => setIngredientPage(p => p + 1)}
                >
                    <Text>Trang sau {"=>"}</Text>
                </TouchableOpacity>
            </View>
            {ingredients.map(i => (
                <TouchableOpacity
                    key={i.uuid}
                    style={CreateFoodStyle.listItem}
                    onPress={() => toggleIngredient(i.name)}
                >
                    <Text style={CreateFoodStyle.listText}>{i.name}</Text>
                    <Text style={CreateFoodStyle.checkbox}>
                        {selectedIngredients.includes(i.name) ? "●" : "○"}
                    </Text>
                </TouchableOpacity>
            ))}

            <View style={CreateFoodStyle.addRow}>
                <TextInput
                    placeholder="Thêm nguyên liệu mới"
                    value={newIngredient}
                    onChangeText={setNewIngredient}
                    style={CreateFoodStyle.addInput}
                />
                <TouchableOpacity
                    style={CreateFoodStyle.addBtn}
                    onPress={createIngredient}
                >
                    <Text style={{ color: "#fff" }}>+</Text>
                </TouchableOpacity>
            </View>

            <TouchableOpacity
                style={CreateFoodStyle.submitBtn}
                onPress={submitFood}
                disabled={loading}>
                <Text style={CreateFoodStyle.submitText}>
                    {loading ? "Đang lưu..." : "Lưu"}
                </Text>
            </TouchableOpacity>
        </ScrollView>
    );
};

export default CreateFood;
