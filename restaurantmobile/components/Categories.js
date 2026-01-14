import { Image, Text, TouchableOpacity, View } from "react-native";
import Apis, { endpoints } from "../utils/Apis";
import { useEffect, useState } from "react";
import HomeStyle from "../styles/HomeStyle";
import MyStyle from "../styles/MyStyle";
import { useNavigation } from "@react-navigation/native";


const Categories = () => {
    const [categories, setCategories] = useState([]);
    const [page, setPage] = useState(1);
    const [next, setNext] = useState();
    const [prev, setPrev] = useState();
    const [loading, setLoading] = useState(false);
    const nav = useNavigation();

    const loadCates = async () => {
        try {
            setLoading(true);

            let url = `${endpoints['categories']}?page=${page}`;

            let res = await Apis.get(url);
            setCategories(res.data.results);
            setNext(res.data.next);
            setPrev(res.data.previous);
        } catch (ex) {
            console.error("Loi:", ex);
        }
    };

    useEffect(() => {
        loadCates(page);
    }, [page]);

    const nextPage = () => {
        if (next) setPage(page + 1);
    };

    const prevPage = () => {
        if (prev) setPage(page - 1);
    };

    return (
    <View>
        <View style={MyStyle.row}>
            {categories.map(item => (
                <TouchableOpacity key={item.uuid} style={HomeStyle.categoryItem} onPress={() => nav.navigate("Search", {
                                                                                                categoryId: item.uuid
                                                                                            })}>
                    <Image
                        source={{ uri: item.image }}
                        style={HomeStyle.categoryImage}
                    />
                    <Text style={HomeStyle.categoryText}>
                        {item.name}
                    </Text>
                </TouchableOpacity>
            ))}
        </View>

        <View style={[HomeStyle.pagination, MyStyle.row]}>
            <TouchableOpacity onPress={prevPage} disabled={!prev} style={HomeStyle.pageBtn}>
                <Text style={HomeStyle.pageBtnText}>
                    {'<'} Trước
                </Text>
            </TouchableOpacity>

            <Text style={HomeStyle.pageText}>
                    Trang {page}
            </Text>

            <TouchableOpacity onPress={nextPage} style={HomeStyle.pageBtn}>
                <Text style={HomeStyle.pageBtnText}>
                    Sau {'>'}
                </Text>
            </TouchableOpacity>
        </View>
    </View>
  );
};

export default Categories;