module Main exposing (..)

import Browser
import Html             exposing (..)
import Html.Attributes  exposing (..)
import Html.Events      exposing (..)
import List             exposing (..)
import String           exposing (..)
import Maybe            exposing (..)
import Hotkeys          exposing (onEnterSend)

type Action = Look
            | Go
            | MoveNorth
            | MoveNorthWest
            | MoveWest
            | MoveSouthWest
            | MoveSouth
            | MoveSouthEast
            | MoveEast
            | MoveNorthEast
            | Take
            | Drop
            | Open
            | Close
            | Read
            | Write
            | Break
            | Lock
            | Unlock
            | NoAction

type alias Usage = List Action
type alias Property = (Action, String)

type alias Object =
    { name          :   String
    , usage         :   Usage
    , properties    :   List Property
    }

type alias Place =
    { position      :   (Int, Int)
    , name          :   String
    , current       :   Bool
    , description   :   String
    , objects       :   List Object
    }

emptyPlace : Place
emptyPlace = Place (0,0) "" False "" []

type alias Map = List (List Place)

type alias World =
    { map   :   Map
    , time  :   Int
    }

type alias Model =
    { display   :   Html Msg
    , world     :   World
    }

type Msg = Input String
         | Output String


--
--  World Map and Design
--

--  00   South-East Corner
place00 : Place
place00 = Place (-1,1)
    "South-East Corner"
    False
    "Nothing interesting here."
    []

--  01   Thekkini
place01 : Place
place01 = Place (0,1)
    "Thekkini"
    False
    """
    You are in what seems to be the thekkini.  The rumours are long of an illam
    right about where you are.  The insidious ambience of the hall draws you
    into its madness, yet you stand there not entering.
    """
    []

--  02  South-West Corner
place02 : Place
place02 = Place (1,1)
    "South-West Corner"
    False
    "Nothing interesting here."
    []

--  10  Kizhakkini
place10 : Place
place10 = Place (-1,0)
    "Kizhakkini"
    False
    "Nothing interesting here."
    []

--  11  Nadumuttam
place11 : Place
place11 = Place (0,0)
    "Nadumuttam"
    True
    """
    The nadumuttam is a place brimming in sunlight.  A pool congeals here during
    the unabated rains of the monsoon.  A tulsi plant (holy basil) stands lonely
    in the centre.  There is something etched on the structure.
    """
    [ Object "inscription"
        [ Look, Read ]
        [ (Look, "There is an inscription here in swash round flowing letters.")
        , (Read, "It reads: Enter Night / Exit God.")
        ]
    ]

--  12  Padinjarini
place12 : Place
place12 = Place (0,1)
    "Padinjarini"
    False
    "Nothing interesting here."
    []

--  20  North-East Corner
place20 : Place
place20 = Place (-1,-1)
    "North-East Corner"
    False
    "Nothing interesting here."
    []

--  21  Vadakkini
place21 : Place
place21 = Place (0,-1)
    "Vadakkini"
    False
    "Nothing interesting here."
    []

--  22  North-West Corner
place22 : Place
place22 = Place (1,-1)
    "North-West Corner"
    False
    "Nothing interesting here."
    []

--  The World Map.
worldMap : Map
worldMap =
    [ [ place00, place01, place02 ]
    , [ place10, place11, place12 ]
    , [ place20, place21, place22 ]
    ]

-- Add text to the model display.
addPrint : Html Msg -> Model -> Model
addPrint message model =
    Model
        (div []
            [ model.display
            , br [] []
            , message
            ]
        )
        model.world

--  The current position in the map.
currentPlace : Map -> Place
currentPlace theMap =
    let
        getPlace xs = List.filter (\x -> x.current) xs
        place = withDefault emptyPlace <| head (List.concat <| List.map getPlace theMap)
    in Place
        place.position
        place.name
        place.current
        place.description
        place.objects

--  Describe a place.
describePlace : Place -> Html Msg
describePlace place =
    div [ class "place-desc" ]
        [ br [] []
        , b [] [ text place.name ]
        , br [] []
        , text place.description
        ]

--  Parse command.
parseOne : String -> Action
parseOne v1 =
    case (toLower v1) of
        "look"      ->  Look
        "north"     ->  MoveNorth
        "south"     ->  MoveSouth
        "west"      ->  MoveWest
        "east"      ->  MoveEast
        _           ->  NoAction

verbOne : Action -> Model -> Model
verbOne v model =
    case v of
        Look -> addPrint (describePlace <| currentPlace model.world.map) model
        _    -> addPrint (text "I do not understand that verb.") model


parseCmd : String -> Model -> Model
parseCmd cmd model =
    let
        cmdList = String.words cmd
    in
        case cmdList of
            v1::_          ->  verbOne (parseOne v1) model
            _              ->  model
            --  v1::v2::[]      ->  parseTwo v1 v2
            --  v1::v2::v3::[]  ->  parseThree v1 v2 v3
    


--
--  Core functions.
--

--  VIEW.
view : Model -> Html Msg
view model =
    div [ id "main" ]
        [ div [ id "display" ]
            [ model.display
            , br [] []
            , div [ id "input-area" ]
                [ label [ id "promp-text" ] [ text ">" ]
                , input [ id "prompt", Hotkeys.onEnterSend Input ] []
                ]
            ]
        ]
    
--  UPDATE.
update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    let
       model_ =
           case msg of
               Input cmd -> parseCmd cmd model
               _         -> model
    in
        (model_, Cmd.none)

--  INITAL MODEL AND INIT.
initDisplay : Html Msg
initDisplay = div [] 
                [   text <|
                    """
                    You are in a nalukettu.  One that had been built perhaps
                    300–400 years ago.  You have happened upon this ancient
                    edifice in a fit of desperate escape.  Who might have
                    built such grand a house for themselves you do not
                    know; you are yet compelled to enter.
                    """
                , br [] []
                , describePlace (currentPlace worldMap)
                ]

initialModel : Model
initialModel = Model initDisplay (World worldMap 0)

init : () -> (Model, Cmd Msg)
init _ = (initialModel, Cmd.none)

--  MAIN.
main : Program () Model Msg
main = Browser.element
    { init = init
    , update = update
    , subscriptions = \_ -> Sub.none
    , view = view
    }
