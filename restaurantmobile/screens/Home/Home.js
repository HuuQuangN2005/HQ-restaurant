import { ScrollView, View } from "react-native";
import HomeStyle from "../../styles/HomeStyle";
import MyStyle from "../../styles/MyStyle";
import ImageBg from "./ImageBg";
import Header from "./Header";
import Categories from "../../components/Categories"
import { Searchbar } from "react-native-paper";
import Apis, { endpoints } from "../../utils/Apis";
import { useCallback, useState } from "react";
import CategoryFoodsSection from "../../components/CategoryFoodsSection";
import { useFocusEffect, useNavigation } from "@react-navigation/native";

const Home = () => {

    const [categories, setCategories] = useState([]);
    const nav = useNavigation();

    const loadCategories = async () => {
        let res = await Apis.get(endpoints['categories']);
        setCategories((res.data.results).slice(0,3));
    };

    useFocusEffect(
        useCallback(() => {
        loadCategories();
        }, [])
    );

    return(
            <ScrollView>
                <View style={HomeStyle.content}>
                    <Header />
                    <ImageBg />
                    <Searchbar
                        style={MyStyle.margin}
                        placeholder="Hôm nay bạn muốn ăn gì..."
                        onPress={() => nav.navigate("Search")}
                    />
                    <Categories />
                    {categories.map(item => (
                        <CategoryFoodsSection
                            key={item.uuid}
                            category={item}
                        />
                    ))}
                </View>
            </ScrollView>
    );
};

export default Home;