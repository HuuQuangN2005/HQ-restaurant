import { ActivityIndicator, Alert, FlatList, Image, ScrollView, Text, TextInput, TouchableOpacity, View } from "react-native";
import MenuStyle from "../../styles/MenuStyle";
import { useEffect, useState } from "react";
import Apis, { endpoints } from "../../utils/Apis";
import { useNavigation, useRoute } from "@react-navigation/native";

const Menu = () => {

    const [categories, setCategories] = useState([]);
    const [foods, setFoods] = useState([]);
    const [compareFoods, setCompareFoods] = useState([]);
    const [cartFoods, setCartFoods] = useState([]);

    const [page, setPage] = useState(1);
    const [loading, setLoading] = useState(false);

    const [keyword, setKeyword] = useState("");
    const [searchType, setSearchType] = useState("name");
    const [maxTime, setMaxTime] = useState("");

    const [ordering, setOrdering] = useState();
    const [showSort, setShowSort] = useState(false);
    const [sortLabel, setSortLabel] = useState("");

    const [showSearchType, setShowSearchType] = useState(false);

    const route = useRoute();
    const nav = useNavigation();

    const cateId = route.params?.categoryId;
    const [categoryId, setCategoryId] = useState(cateId);
    const isSearching = keyword !== "" || maxTime !== "";
    const [hasNext, setHasNext] = useState(true);

    const loadCates = async () => {
        let all = [];
    let page = 1;

    while (true) {
        let res = await Apis.get(endpoints['categories'], { params: { page } });
            all = [...all, ...res.data.results];
            if (!res.data.next) break;
            page++;
        }
        setCategories(all);
    }

    const loadFoods = async () => {
        setLoading(true)
        try {
            let params = { page };
            if (keyword) {
                params.q = keyword; 
            }

            if (categoryId) {
                params.category = categoryId;
            }

            if (ordering){
                params.ordering = ordering;
            }

            if (searchType == "time" && maxTime)
                params.max_time=maxTime

            let res = await Apis.get(endpoints['foods'], {params})
            if (page === 1){
                setFoods(res.data.results);
            } else {
                setFoods(prev => [...prev, ...res.data.results])
            }
            setHasNext(!!res.data.next);

        } catch (ex){
            console.log(ex);
        } finally {
            setLoading(false)
        }
    }

    const toggleCompare = (food) => {
        setCompareFoods(prev => {
            const exists = prev.find(f => f.uuid === food.uuid);
            if (exists) {
                return prev.filter(f => f.uuid !== food.uuid);
            }
            if (prev.length >= 2) {
                Alert.alert("Thông báo","Chỉ được so sánh tối đa 2 món");
                return prev;
            }
            return [...prev, food];
        });
    };

    const toggleCart = (food) => {
        setCartFoods(prev => {
            const exists = prev.find(f => f.uuid === food.uuid)
            if (exists) 
                return prev.filter(f => f.uuid !== food.uuid)
            return [...prev, food]
        })
    }

    useEffect(() => {
        let timer = setTimeout(() => {
            if (page > 0)
                loadFoods();
        }, 500);

        return () => clearTimeout(timer);
    }, [keyword, categoryId, maxTime, ordering]);

    useEffect(() => {
        if (page > 1)
            loadFoods();
    }, [page]);

    
    useEffect(() => {
        if (cateId) {
            setCategoryId(cateId);
            setPage(1);
        }
    }, [cateId]);

    useEffect(() => {
        loadCates();
    },[])

    useEffect(() => {
        setFoods([]);
        setPage(1);
    }, [keyword, categoryId, maxTime]);

    const loadMore = () => {
        if (loading) return;
        if (!hasNext) return;
        if (isSearching) return;

        setPage(prev => prev + 1);
    };

    const SORT_OPTIONS = [
        { label: "Tên A-Z", value: "name" },
        { label: "Giá giảm dần", value: "-price" },
        { label: "Giá tăng dần", value: "price" },
        { label: "Thời gian phục vụ", value: "cook_time" },
    ];

    const RenderSearchType = () => {
        switch(searchType){
            case "name":
                return (
                    <TextInput
                        placeholder="Tìm theo tên món ăn"
                        style={MenuStyle.search}
                        value={keyword} onChangeText={(text) => {
                                                                    setKeyword(text);
                                                                    setPage(1);
                                                                }}
                    />
                );
            
            case "time":
                return(
                    <TextInput
                        placeholder="Tìm theo thời gian phục vụ (phút)"
                        keyboardType="numeric"
                        style={MenuStyle.search}
                        value={maxTime} onChangeText={(text) => {
                                                                    setMaxTime(text);
                                                                    setPage(1);
                                                                }}
                    />
                )
            default:
                return null;
        }
    }

    const renderSearchTypeDropdown = () => {
        if (!showSearchType) return null;

        return (
            <View style={MenuStyle.searchTypeOverlay}>
                <View style={MenuStyle.searchTypeDropdown}>
                    <TouchableOpacity style={[MenuStyle.searchTypeItem, searchType === "name" && MenuStyle.searchTypeItemActive,]}
                        onPress={() => {setSearchType("name"); setMaxTime(""); setShowSearchType(false); setPage(1);}}>
                        <Text>Tên món</Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={[MenuStyle.searchTypeItem, searchType === "time" && MenuStyle.searchTypeItemActive,]}
                        onPress={() => {setSearchType("time"); setKeyword(""); setShowSearchType(false); setPage(1);}}>
                        <Text>Thời gian phục vụ</Text>
                    </TouchableOpacity>
                </View>
            </View>
        );
    };


    return(
        <View style={{ flex: 1 }}>
            <FlatList
                data={foods}
                keyExtractor={item => item.uuid}
                onEndReached={loadMore}
                onEndReachedThreshold={0.2}
                ListFooterComponent={loading && <ActivityIndicator size="large" />}
                ListHeaderComponent={
                    <View>
                        <Text style={MenuStyle.title}>Thực đơn</Text>
                        <View style={MenuStyle.searchTypeWrapper}>
                            <TouchableOpacity style={MenuStyle.searchTypeButton} onPress={() => setShowSearchType(prev => !prev)}>
                                <Text style={MenuStyle.searchTypeButtonText}>
                                    Tìm theo: {searchType === "name" ? "Tên món" : "Thời gian"}
                                </Text>
                            </TouchableOpacity>
                            {renderSearchTypeDropdown()}
                        </View>

                        {RenderSearchType()}
                        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={MenuStyle.categoryList}>
                            <TouchableOpacity
                                style={[MenuStyle.cateFilter, !categoryId && MenuStyle.cateActive]}
                                onPress={() => {setCategoryId(null); setPage(1)}}>
                                <Text>Tất cả</Text>
                            </TouchableOpacity>

                            {categories.map(c => (
                                <TouchableOpacity
                                    key={c.uuid}
                                    style={[MenuStyle.cateFilter, categoryId === c.uuid && MenuStyle.cateActive]}
                                    onPress={() => {setCategoryId(c.uuid); setPage(1)}}>
                                    <Text>{c.name}</Text>
                                </TouchableOpacity>
                            ))}
                        </ScrollView>

                        <View style={MenuStyle.sortRowWrapper}>
                            <View style={MenuStyle.sortRowHeader}>
                                <TouchableOpacity style={MenuStyle.sortButton} onPress={() => setShowSort(prev => !prev)}>
                                    <Text style={MenuStyle.sortButtonText}>
                                        Sắp xếp: {sortLabel || "Mặc định"}
                                    </Text>
                                </TouchableOpacity>

                                <TouchableOpacity style={MenuStyle.compareTopBtn} onPress={() => {
                                        if (compareFoods.length !== 2) {
                                            Alert.alert("Cảnh báo!!","Chọn đúng 2 món để so sánh");
                                            return;
                                        }
                                        nav.navigate("CompareFood", { foods: compareFoods });
                                    }}>

                                    <Text style={MenuStyle.compareTopText}>
                                        So sánh ({compareFoods.length}/2)
                                    </Text>
                                </TouchableOpacity>
                            </View>
                            {showSort && (
                                <View style={MenuStyle.sortDropdown}>
                                    {SORT_OPTIONS.map(opt => (
                                        <TouchableOpacity
                                            key={opt.value}
                                            style={MenuStyle.sortItem}
                                            onPress={() => {
                                                setOrdering(opt.value);
                                                setSortLabel(opt.label);
                                                setShowSort(false);
                                                setPage(1);
                                            }}
                                        >
                                            <Text>{opt.label}</Text>
                                        </TouchableOpacity>
                                    ))}
                                </View>
                            )}
                        </View>
                    </View>
                }
                renderItem={({ item }) => {
                    const selected = compareFoods.some(f => f.uuid === item.uuid);
                    const inCart = cartFoods.some(f => f.uuid === item.uuid);
                    return (
                        <View
                            style={[MenuStyle.foodItem, selected && MenuStyle.foodItemSelected]}>
                            <TouchableOpacity key={item.uuid} activeOpacity={0.7} onPress={() => nav.navigate("FoodDetail", { foodUuid: item.uuid })}>
                                <Image source={{ uri: item.image }} style={MenuStyle.foodImage} />
                            </TouchableOpacity> 

                            <View style={MenuStyle.foodInfo}>
                                <Text style={MenuStyle.foodName}>{item.name}</Text>
                            </View>

                            <Text style={MenuStyle.foodPrice}>
                                {Number(item.price).toLocaleString("vi-VN")}đ
                            </Text>

                            <Text style={MenuStyle.foodMeta}>
                                {item.cook_time} phút
                            </Text>

                            <View style={MenuStyle.actionRow}>
                                <TouchableOpacity
                                    onPress={() => toggleCompare(item)}
                                    style={[MenuStyle.compareBtn, selected && MenuStyle.compareBtnSelected]}>

                                    <Text style={[MenuStyle.compareText, selected && MenuStyle.compareTextSelected]}>
                                        {selected ? "Đã chọn" : "So sánh"}
                                    </Text>
                                </TouchableOpacity>

                                <TouchableOpacity
                                    onPress={() => toggleCart(item)}
                                    style={[MenuStyle.addCartPlus, inCart && MenuStyle.addCartPlusActive]}>

                                    <Text style={[MenuStyle.addCartPlusText, inCart && MenuStyle.addCartPlusTextActive]}>
                                        {inCart ? "✓" : "+"}
                                    </Text>
                                </TouchableOpacity>
                            </View>
                        </View>
                    );
                }}
            />
            {cartFoods.length > 0 && (
                <TouchableOpacity
                    onPress={() =>
                        nav.navigate("Checkout", {
                            cartFoods: cartFoods
                        })
                    }
                    style={MenuStyle.compareFooterBtn}>

                    <Text style={MenuStyle.compareFooterText}>
                        Thanh toán
                    </Text>
                </TouchableOpacity>
            )}
        </View>
    )
}

export default Menu;