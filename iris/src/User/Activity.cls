Class User.Activity Extends %Persistent [ SqlTableName = Activity ]
{

// Create properties for this csv

// place,activity_type,activity,activity_description,full_activity

// south australia,Exploring Adelaide,Cultural Attractions," South Australia’s capital city, Adelaide, is known for its cultural venues such as the Art Gallery of South Australia, the South Australian Museum, and the Adelaide Festival Centre","Exploring Adelaide - Cultural Attractions -  South Australia’s capital city, Adelaide, is known for its cultural venues such as the Art Gallery of South Australia, the South Australian Museum, and the Adelaide Festival Centre"

// south australia,Wine Regions,Barossa Valley," Known for its world-renowned wineries, this region offers wine tasting tours, gourmet food experiences, and picturesque vineyards","Wine Regions - Barossa Valley -  Known for its world-renowned wineries, this region offers wine tasting tours, gourmet food experiences, and picturesque vineyards"

Property Place As %String(MAXLEN = 500);

Property Type As %String(MAXLEN = 500);

Property Name As %String(MAXLEN = 500);

Property Description As %String(MAXLEN = 3641144);

Property FullActivity As %String(MAXLEN = 3641144);

Index FullActivityIFind On (FullActivity) As %iFind.Index.Basic;

Property FullActivityvector As %Library.Vector(DATATYPE = "DOUBLE", LEN = 384) [ SqlColumnNumber = 9, SqlFieldName = FullActivity_vector ];

Storage Default
{
<Data name="ActivityDefaultData">
<Value name="1">
<Value>%%CLASSNAME</Value>
</Value>
<Value name="2">
<Value>Place</Value>
</Value>
<Value name="3">
<Value>Type</Value>
</Value>
<Value name="4">
<Value>Name</Value>
</Value>
<Value name="5">
<Value>Description</Value>
</Value>
<Value name="6">
<Value>FullActivity</Value>
</Value>
<Value name="7">
<Value>FullActivityvector</Value>
</Value>
</Data>
<DataLocation>^User.ActivityD</DataLocation>
<DefaultData>ActivityDefaultData</DefaultData>
<IdLocation>^User.ActivityD</IdLocation>
<IndexLocation>^User.ActivityI</IndexLocation>
<StreamLocation>^User.ActivityS</StreamLocation>
<Type>%Storage.Persistent</Type>
}

}
