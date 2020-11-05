import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import {StocksView} from './components/views/stocks/StocksView'
import {StockDetailsView} from './components/views/stockDetails/StockDetailsView'

export const App = () => {
    return (
        <Router>
            <Switch>
                <Route exact path="/">
                    <Redirect to="/stocks" />
                </Route>
                <Route path="/stocks" component={StocksView}/>
                <Route path="/stockdetails/:symbol" component={StockDetailsView}/>
            </Switch>
        </Router>
    )
}


export default App;
